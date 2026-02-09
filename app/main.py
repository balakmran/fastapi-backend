from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from structlog import get_logger

from app.api import api_router
from app.core.exception_handlers import add_exception_handlers
from app.core.logging import setup_logging
from app.core.middlewares import configure_middlewares
from app.core.openapi import OPENAPI_PARAMETERS, set_openapi_generator
from app.core.telemetry import setup_opentelemetry
from app.db.session import close_db, init_db

setup_logging()
logger = get_logger()


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

    # Setup Observability
    setup_opentelemetry(app)

    # Mount static files
    app.mount("/static", StaticFiles(directory="app/static"), name="static")

    app.include_router(api_router)

    return app


app = create_app()
