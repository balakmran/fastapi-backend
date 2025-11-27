from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI

from app.api import api_router
from app.core.exception_handlers import add_exception_handlers
from app.core.logging import setup_logging
from app.core.middlewares import configure_middlewares
from app.core.openapi import OPENAPI_PARAMETERS, set_openapi_generator
from app.db.session import close_db, init_db

setup_logging()
logger = structlog.get_logger()


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
        """Manage application lifecycle."""
        logger.info("Startup")
        init_db()
        yield
        await close_db()
        logger.info("Shutdown")

    app = FastAPI(lifespan=lifespan, **OPENAPI_PARAMETERS)
    set_openapi_generator(app)
    add_exception_handlers(app)
    configure_middlewares(app)

    app.include_router(api_router)

    @app.get("/")
    async def root() -> dict[str, str]:
        """Root endpoint to verify the application is running."""
        return {"message": "Welcome to FastAPI Backend"}

    @app.get("/health", include_in_schema=False)
    async def health() -> dict[str, str]:
        """Health check endpoint."""
        return {"status": "ok"}

    return app


app = create_app()
