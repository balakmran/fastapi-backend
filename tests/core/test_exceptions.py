import pytest
from fastapi import FastAPI, status
from httpx import ASGITransport, AsyncClient

from app.core.exception_handlers import add_exception_handlers
from app.core.exceptions import AppError, InternalServerError


def test_app_error_init() -> None:
    """Test AppError initialization."""
    err = AppError(
        message="Test Error",
        status_code=status.HTTP_400_BAD_REQUEST,
        headers={"X-Error": "True"},
    )
    assert err.message == "Test Error"
    assert err.status_code == status.HTTP_400_BAD_REQUEST
    assert err.headers == {"X-Error": "True"}


def test_internal_server_error_init() -> None:
    """Test InternalServerError initialization."""
    err = InternalServerError()
    assert err.message == "Internal Server Error"
    assert err.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert err.headers is None

    err_custom = InternalServerError(message="Custom Error", headers={"X-Custom": "1"})
    assert err_custom.message == "Custom Error"
    assert err_custom.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert err_custom.headers == {"X-Custom": "1"}


@pytest.mark.asyncio
async def test_exception_handlers() -> None:
    """Test exception handlers via a temporary app."""
    app = FastAPI()
    add_exception_handlers(app)

    @app.get("/app_error")
    async def raise_app_error() -> None:
        raise AppError(
            message="Custom App Error", status_code=status.HTTP_418_IM_A_TEAPOT
        )

    @app.get("/generic_error")
    async def raise_generic_error() -> None:
        raise ValueError("Something went wrong")

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        # Test AppError handler
        response = await ac.get("/app_error")
        assert response.status_code == status.HTTP_418_IM_A_TEAPOT
        assert response.json() == {"detail": "Custom App Error"}

        # Test generic exception handler (should raise exception)
        with pytest.raises(ValueError):
            await ac.get("/generic_error")
