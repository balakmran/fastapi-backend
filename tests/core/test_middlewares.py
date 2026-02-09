from unittest.mock import patch

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from app.core.config import settings
from app.core.middlewares import (
    configure_cors,
    configure_middlewares,
    configure_trusted_hosts,
)


def test_configure_cors_enabled() -> None:
    """Test CORS middleware configuration when origins are enabled."""
    app = FastAPI()

    # Patch settings to enable CORS
    with patch.object(
        settings, "BACKEND_CORS_ORIGINS", ["http://localhost:3000"]
    ):
        configure_cors(app)

        # Verify CORSMiddleware is added
        has_cors = any(m.cls == CORSMiddleware for m in app.user_middleware)
        assert has_cors


def test_configure_cors_disabled() -> None:
    """Test CORS middleware when origins are disabled."""
    app = FastAPI()

    # Patch settings to disable CORS
    with patch.object(settings, "BACKEND_CORS_ORIGINS", []):
        configure_cors(app)

        # Verify CORSMiddleware is NOT added
        has_cors = any(m.cls == CORSMiddleware for m in app.user_middleware)
        assert not has_cors


def test_configure_trusted_hosts() -> None:
    """Test TrustedHost middleware configuration."""
    app = FastAPI()
    configure_trusted_hosts(app)

    # Verify TrustedHostMiddleware is added
    has_trusted_host = any(
        m.cls == TrustedHostMiddleware for m in app.user_middleware
    )
    assert has_trusted_host


def test_configure_middlewares() -> None:
    """Test that configure_middlewares configures all middlewares."""
    app = FastAPI()

    with patch.object(
        settings, "BACKEND_CORS_ORIGINS", ["http://localhost:3000"]
    ):
        configure_middlewares(app)

        # Verify both middlewares are added
        has_cors = any(m.cls == CORSMiddleware for m in app.user_middleware)
        has_trusted_host = any(
            m.cls == TrustedHostMiddleware for m in app.user_middleware
        )

        assert has_cors
        assert has_trusted_host
