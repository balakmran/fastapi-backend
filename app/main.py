from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api import api_router
from app.core.exception_handlers import add_exception_handlers
from app.core.logging import setup_logging
from app.core.middlewares import configure_middlewares
from app.core.openapi import OPENAPI_PARAMETERS, set_openapi_generator
from app.core.telemetry import setup_opentelemetry
from app.db.session import create_db_engine


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    setup_logging()

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
        """Manage application lifecycle."""
        app.state.engine = create_db_engine()
        yield
        await app.state.engine.dispose()

    app = FastAPI(lifespan=lifespan, **OPENAPI_PARAMETERS)
    set_openapi_generator(app)
    add_exception_handlers(app)
    configure_middlewares(app)

    # Setup Observability
    setup_opentelemetry(app)

    # Mount static files (use absolute path)
    base_dir = Path(__file__).resolve().parent
    app.mount(
        "/static", StaticFiles(directory=base_dir / "static"), name="static"
    )

    app.include_router(api_router)

    return app


app = create_app()
