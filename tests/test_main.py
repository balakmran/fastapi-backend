from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture(autouse=True)
def mock_db_lifecycle():
    """Mock database lifecycle events to avoid connection attempts."""
    mock_engine = MagicMock()
    mock_engine.dispose = AsyncMock()

    with patch("app.db.session.create_db_engine", return_value=mock_engine):
        yield


def test_lifespan():
    """Test lifespan events (startup/shutdown)."""
    app = create_app()

    # TestClient triggers lifespan events on enter/exit
    with TestClient(app, base_url="http://test") as client:
        response = client.get("/health")
        assert response.status_code == status.HTTP_200_OK
