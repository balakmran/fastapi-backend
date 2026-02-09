from unittest.mock import AsyncMock

import pytest
from fastapi import status
from httpx import ASGITransport, AsyncClient

from app.db.session import get_session
from app.main import create_app


@pytest.mark.asyncio
async def test_root():
    """Test the root endpoint."""
    app = create_app()
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/")

    assert response.status_code == status.HTTP_200_OK
    assert "text/html" in response.headers["content-type"]
    assert "All Systems Operational" in response.text


@pytest.mark.asyncio
async def test_health():
    """Test the health endpoint."""
    app = create_app()
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_ready_success():
    """Test the readiness endpoint when DB is available."""
    app = create_app()

    # Mock the session dependency
    async def mock_get_session():
        mock_session = AsyncMock()
        mock_session.exec = AsyncMock(return_value=True)
        yield mock_session

    app.dependency_overrides[get_session] = mock_get_session

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/ready")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "ready"}


@pytest.mark.asyncio
async def test_ready_failure():
    """Test the readiness endpoint when DB is unavailable."""
    app = create_app()

    # Mock the session dependency to raise exception
    async def mock_get_session():
        mock_session = AsyncMock()
        mock_session.exec = AsyncMock(
            side_effect=Exception("DB Connection Error")
        )
        yield mock_session

    app.dependency_overrides[get_session] = mock_get_session

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/ready")

    assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
    assert response.json()["detail"] == "Database connection failed"
