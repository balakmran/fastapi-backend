import re
from http import HTTPStatus
from typing import Any

import structlog
from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import Response

from app.core.exceptions import QuoinError, QuoinRequestValidationError
from app.core.schemas import ProblemDetail

logger = structlog.get_logger(__name__)

_PROBLEM_MEDIA_TYPE = "application/problem+json"

# Cap on the serialised length of a reflected `input` value in a 422
# body, so a validation error never echoes an unbounded amount of
# client-supplied data back into the response.
_MAX_INPUT_CHARS = 200

# CPython's HTTPStatus.phrase wording tracks RFC updates (e.g. 422's
# phrase changed from "Unprocessable Entity" to "Unprocessable Content"),
# so deriving titles from it would make the response body depend on
# which Python version is running the server. Pin the phrases QuoinAPI
# actually raises so the RFC 9457 `title` field is stable across the
# supported interpreter range.
_PROBLEM_TITLES = {
    HTTPStatus.UNPROCESSABLE_ENTITY: "Unprocessable Content",
}


def _problem_type(exc: Exception) -> str:
    """Derive a URN problem type from the exception class name."""
    name = type(exc).__name__
    snake = re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()
    return f"urn:quoin:error:{snake}"


def _problem_title(status_code: int) -> str:
    """Return the standard HTTP reason phrase for a status code."""
    try:
        status = HTTPStatus(status_code)
    except ValueError:
        return "Error"
    return _PROBLEM_TITLES.get(status, status.phrase)


def _problem_response(
    problem: ProblemDetail,
    status_code: int,
    headers: dict[str, str] | None = None,
) -> Response:
    """Serialize a ProblemDetail into an application/problem+json response."""
    return Response(
        content=problem.model_dump_json(exclude_none=True),
        status_code=status_code,
        media_type=_PROBLEM_MEDIA_TYPE,
        headers=headers,
    )


async def quoin_exception_handler(request: Request, exc: Any) -> Response:
    """Handle QuoinError exceptions."""
    quoin_exc: QuoinError = exc
    logger.warning(
        "quoin_error",
        status_code=quoin_exc.status_code,
        message=quoin_exc.message,
        path=request.url.path,
    )
    problem = ProblemDetail(
        type=_problem_type(quoin_exc),
        title=_problem_title(quoin_exc.status_code),
        status=quoin_exc.status_code,
        detail=quoin_exc.message,
        instance=request.url.path,
    )
    return _problem_response(problem, quoin_exc.status_code, quoin_exc.headers)


async def unhandled_exception_handler(request: Request, exc: Any) -> Response:
    """Handle any exception not caught by a more specific handler.

    Guarantees that even bare ``KeyError``s or non-transport ``httpx``
    errors surface as RFC 9457 ``application/problem+json`` responses
    rather than Starlette's default ``text/plain`` 500. The internal
    exception message and traceback are logged but never leaked to the
    client.
    """
    logger.exception(
        "unhandled_exception",
        exc_type=type(exc).__name__,
        path=request.url.path,
    )
    problem = ProblemDetail(
        type="urn:quoin:error:internal_server_error",
        title=_problem_title(500),
        status=500,
        detail="Internal Server Error",
        instance=request.url.path,
    )
    return _problem_response(problem, 500)


def _truncate_input(value: Any) -> Any:
    """Cap the serialised length of a reflected validation `input` value.

    Args:
        value: A JSON-safe value (already passed through
            ``jsonable_encoder``).

    Returns:
        ``value`` unchanged if its string form fits within
        ``_MAX_INPUT_CHARS``, else a truncated string with an ellipsis.
    """
    text = value if isinstance(value, str) else repr(value)
    if len(text) <= _MAX_INPUT_CHARS:
        return value
    return text[:_MAX_INPUT_CHARS] + "…"


def _sanitize_validation_errors(
    errors: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Make validation errors JSON-safe and trim what they reveal.

    Pydantic's documented custom-validation idiom — a ``field_validator``
    raising ``ValueError`` or ``AssertionError`` — puts the raised
    exception object itself under ``ctx.error``. That is not
    JSON-serializable, so building the response with a bare
    ``model_dump_json`` raises and this 422 path would itself surface as
    an internal 500. ``jsonable_encoder`` is FastAPI's own fallback for
    this: it stringifies anything it cannot otherwise encode.

    Also drops ``url`` (a link into Pydantic's own docs, not useful to an
    API client) and truncates ``input`` (see ``_truncate_input``), so a
    validation error never echoes an unbounded amount of client-supplied
    data — or a stray secret pasted into the wrong field — back into the
    response body.

    Args:
        errors: Raw error dicts from ``exc.errors()``.

    Returns:
        JSON-safe error dicts with `url` removed and `input` truncated.
    """
    sanitized: list[dict[str, Any]] = []
    for error in jsonable_encoder(errors):
        error.pop("url", None)
        if "input" in error:
            error["input"] = _truncate_input(error["input"])
        sanitized.append(error)
    return sanitized


async def validation_exception_handler(request: Request, exc: Any) -> Response:
    """Handle Pydantic and FastAPI request validation errors."""
    errors = _sanitize_validation_errors(exc.errors())
    problem = ProblemDetail(
        type="urn:quoin:error:validation_error",
        title=_problem_title(422),
        status=422,
        detail="Request validation failed",
        instance=request.url.path,
        errors=errors,
    )
    return _problem_response(problem, 422)


def add_exception_handlers(app: FastAPI) -> None:
    """Add exception handlers to the application."""
    app.add_exception_handler(
        QuoinRequestValidationError, validation_exception_handler
    )
    app.add_exception_handler(QuoinError, quoin_exception_handler)
    app.add_exception_handler(
        RequestValidationError, validation_exception_handler
    )
    app.add_exception_handler(Exception, unhandled_exception_handler)
