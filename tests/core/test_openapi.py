import importlib
from typing import Any

import pytest
from fastapi import FastAPI

from app.core import config as config_module
from app.core import openapi as openapi_module
from app.core.config import Environment
from app.core.openapi import (
    DEFAULT_ERROR_RESPONSES,
    PROBLEM_MEDIA_TYPE,
    error_responses,
    set_openapi_generator,
)
from app.core.schemas import ProblemDetail
from app.main import create_app

_PROBLEM_REF = "#/components/schemas/ProblemDetail"


@pytest.fixture
def schema() -> dict[str, Any]:
    """The generated OpenAPI schema for the real application."""
    return create_app().openapi()


def test_set_openapi_generator() -> None:
    """Test set_openapi_generator attaches the function."""
    app = FastAPI()
    set_openapi_generator(app)

    # The app.openapi attribute should be a bound method or partial
    # We can verify that calling app.openapi() returns a schema
    schema = app.openapi()
    assert schema is not None
    assert schema["openapi"] == "3.1.0"

    # Call it again to test caching (line 70 coverage)
    schema2 = app.openapi()
    assert schema2 is schema


def test_openapi_url_disabled_in_production() -> None:
    """B9 regression: /openapi.json is hidden in production like /docs.

    Reads/writes ``config_module.settings`` (not a name captured at
    import time) since other tests reload ``app.core.config`` and
    rebind its module-level ``settings`` to a fresh instance.
    """
    original_env = config_module.settings.ENV
    try:
        config_module.settings.ENV = Environment.production
        importlib.reload(openapi_module)
        assert openapi_module.OPENAPI_PARAMETERS["openapi_url"] is None
        assert openapi_module.OPENAPI_PARAMETERS["docs_url"] is None
        assert openapi_module.OPENAPI_PARAMETERS["redoc_url"] is None
    finally:
        config_module.settings.ENV = original_env
        importlib.reload(openapi_module)


def test_error_responses_builds_problem_detail_models() -> None:
    """Each requested code maps to the RFC 9457 model."""
    responses = error_responses(404, 409)

    assert set(responses) == {404, 409}
    assert responses[404]["model"] is ProblemDetail
    assert responses[409]["model"] is ProblemDetail
    assert responses[404]["description"] == "Not Found"


def test_error_responses_applies_description_overrides() -> None:
    """Routes can say something better than the reason phrase."""
    responses = error_responses(404, 409, descriptions={404: "User not found"})

    assert responses[404]["description"] == "User not found"
    # Codes without an override keep the generic description.
    assert responses[409]["description"] == "Conflict"


def test_error_responses_rejects_undocumented_code() -> None:
    """An unknown status code fails loudly rather than silently."""
    with pytest.raises(KeyError):
        error_responses(418)


def test_default_error_responses_cover_auth_and_validation() -> None:
    """Every authenticated route documents these four codes."""
    assert set(DEFAULT_ERROR_RESPONSES) == {401, 403, 422, 500}


def test_error_responses_use_problem_media_type(
    schema: dict[str, Any],
) -> None:
    """Error bodies are advertised as application/problem+json.

    The wire format comes from ``app.core.exception_handlers``; this
    asserts the documented contract matches it.
    """
    seen = 0
    for path_item in schema["paths"].values():
        for operation in path_item.values():
            for code, response in operation["responses"].items():
                if not code.startswith(("4", "5")):
                    continue
                content = response.get("content")
                if content is None:
                    continue
                assert list(content) == [PROBLEM_MEDIA_TYPE], (
                    f"{code} should use {PROBLEM_MEDIA_TYPE}"
                )
                assert content[PROBLEM_MEDIA_TYPE]["schema"]["$ref"] == (
                    _PROBLEM_REF
                )
                seen += 1
    assert seen > 0, "no error responses found to check"


def test_validation_errors_documented_as_problem_detail(
    schema: dict[str, Any],
) -> None:
    """422 is a ProblemDetail, not FastAPI's HTTPValidationError.

    The validation handler returns RFC 9457 with an ``errors`` array,
    so the default FastAPI 422 model would mislead generated SDKs.
    """
    for path_item in schema["paths"].values():
        for operation in path_item.values():
            response = operation["responses"]["422"]
            ref = response["content"][PROBLEM_MEDIA_TYPE]["schema"]["$ref"]
            assert ref == _PROBLEM_REF


def test_fastapi_validation_schemas_not_exposed(
    schema: dict[str, Any],
) -> None:
    """The unused default validation models are gone from components."""
    components = schema["components"]["schemas"]

    assert "HTTPValidationError" not in components
    assert "ValidationError" not in components
    assert "ProblemDetail" in components


def test_success_responses_keep_json_media_type(
    schema: dict[str, Any],
) -> None:
    """The rewrite only touches error bodies."""
    created = schema["paths"]["/api/v1/users/"]["post"]["responses"]["201"]

    assert list(created["content"]) == ["application/json"]


def test_media_type_rewrite_skips_non_operation_keys() -> None:
    """Path-level keys like ``parameters`` are not treated as operations.

    A path item may hold ``parameters``/``summary`` alongside its
    operations. Those are not dicts of responses, so the rewrite must
    skip them rather than walking into them.
    """
    schema: dict[str, Any] = {
        "paths": {
            "/things": {
                "parameters": [{"name": "trace", "in": "query"}],
                "summary": "Things",
                "get": {
                    "responses": {
                        "404": {
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": _PROBLEM_REF}
                                }
                            }
                        }
                    }
                },
            }
        }
    }

    openapi_module._use_problem_media_type(schema)

    path_item: dict[str, Any] = schema["paths"]["/things"]
    assert path_item["parameters"] == [{"name": "trace", "in": "query"}]
    assert path_item["summary"] == "Things"
    content = path_item["get"]["responses"]["404"]["content"]
    assert list(content) == [PROBLEM_MEDIA_TYPE]


def test_no_content_response_has_no_body(schema: dict[str, Any]) -> None:
    """A 204 stays bodyless rather than gaining a problem+json entry."""
    deleted = schema["paths"]["/api/v1/users/{user_id}"]["delete"]
    no_content = deleted["responses"]["204"]

    assert "content" not in no_content
