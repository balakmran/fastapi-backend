import structlog
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.exceptions import AppError

logger = structlog.get_logger()


async def app_exception_handler(
    request: Request, exc: AppError
) -> JSONResponse:
    """Handle AppError exceptions."""
    logger.warning(
        "app_error",
        message=exc.message,
        status_code=exc.status_code,
        path=request.url.path,
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
        headers=exc.headers,
    )


def add_exception_handlers(app: FastAPI) -> None:
    """Add exception handlers to the application."""
    app.add_exception_handler(AppError, app_exception_handler)  # type: ignore
