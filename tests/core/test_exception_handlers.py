import pydantic
import pytest
from fastapi import status
from httpx import ASGITransport, AsyncClient
from pydantic import field_validator

from app.core.exception_handlers import _sanitize_validation_errors
from app.main import create_app


class _InternalModel(pydantic.BaseModel):
    """Stand-in for an internal model whose construction can fail."""

    n: int


@pytest.mark.asyncio
async def test_bare_pydantic_validation_error_returns_500_not_422() -> None:
    """Internal ValidationError (not a request body) falls through to 500."""
    app = create_app()

    @app.get("/test-internal-validation-bug")
    async def _buggy() -> dict[str, str]:
        _InternalModel.model_validate({"n": "not-an-int"})
        return {}

    transport = ASGITransport(app=app, raise_app_exceptions=False)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/test-internal-validation-bug")

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.headers["content-type"] == "application/problem+json"
    body = response.json()
    assert body["type"] == "urn:quoin:error:internal_server_error"
    assert body["detail"] == "Internal Server Error"


class _ValidatedBody(pydantic.BaseModel):
    """Request body with a field_validator that can raise on bad input."""

    name: str

    @field_validator("name")
    @classmethod
    def _reject_bad(cls, value: str) -> str:
        """Reject the sentinel value; Pydantic's documented raise idiom."""
        if value == "bad":
            raise ValueError("name may not be 'bad'")
        return value


@pytest.mark.asyncio
async def test_request_validator_raising_value_error_returns_422() -> None:
    """B2 regression: a raising field_validator yields 422, not 500.

    Pydantic puts the raised exception itself under ``ctx.error`` for
    this case, which crashed the 422 handler's JSON serialisation before
    the fix and surfaced as an internal 500.
    """
    app = create_app()

    @app.post("/test-validated-body")
    async def _endpoint(body: _ValidatedBody) -> dict[str, str]:
        return {"name": body.name}

    transport = ASGITransport(app=app, raise_app_exceptions=False)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/test-validated-body", json={"name": "bad"})

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert response.headers["content-type"] == "application/problem+json"
    body = response.json()
    assert body["type"] == "urn:quoin:error:validation_error"
    error = body["errors"][0]
    assert "url" not in error
    assert "may not be 'bad'" in error["msg"]


@pytest.mark.asyncio
async def test_validation_error_input_is_truncated() -> None:
    """A validation error never echoes an unbounded `input` value."""
    app = create_app()

    @app.post("/test-long-input")
    async def _endpoint(body: _InternalModel) -> dict[str, int]:
        return {"n": body.n}

    transport = ASGITransport(app=app, raise_app_exceptions=False)
    long_value = "x" * 5000
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/test-long-input", json={"n": long_value})

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    error = response.json()["errors"][0]
    assert len(error["input"]) < len(long_value)
    assert error["input"].endswith("…")


@pytest.mark.asyncio
async def test_oversize_non_string_input_is_dropped_not_retyped() -> None:
    """An over-long structured `input` is dropped, never turned into a str.

    Truncating a dict or list to a string would make the JSON type of
    `errors[].input` depend on the value's size — an object for a small
    payload, a string for a large one — and the truncated Python `repr`
    isn't valid JSON for a client to parse anyway.
    """
    app = create_app()

    @app.post("/test-structured-input")
    async def _endpoint(body: _InternalModel) -> dict[str, int]:
        return {"n": body.n}

    transport = ASGITransport(app=app, raise_app_exceptions=False)
    small = {"a": 1}
    large = {f"field_{i}": i for i in range(50)}
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        small_response = await ac.post(
            "/test-structured-input", json={"n": small}
        )
        large_response = await ac.post(
            "/test-structured-input", json={"n": large}
        )

    # Small enough to reflect: kept, and still a JSON object.
    small_error = small_response.json()["errors"][0]
    assert small_error["input"] == small

    # Too large: the key is absent rather than holding a stringified dict.
    large_error = large_response.json()["errors"][0]
    assert "input" not in large_error


def test_sanitize_validation_errors_tolerates_missing_input() -> None:
    """An error dict without an `input` key passes through untouched.

    Not every error shape Pydantic can produce carries `input` (e.g. one
    hand-built by a custom handler), so the sanitizer must not assume
    the key is always present.
    """
    errors = [{"loc": ("body", "name"), "msg": "field required", "url": "x"}]

    sanitized = _sanitize_validation_errors(errors)

    assert sanitized == [{"loc": ["body", "name"], "msg": "field required"}]
