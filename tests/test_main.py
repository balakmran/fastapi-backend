from unittest.mock import patch

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture(autouse=True)
def mock_db_lifecycle():
    """Mock database lifecycle events to avoid connection attempts."""
    with (
        patch("tests.conftest.init_db"),
        patch("tests.conftest.close_db"),
        patch("app.main.init_db"),
        patch("app.main.close_db"),
    ):
        yield


def test_lifespan():
    """Test lifespan events (startup/shutdown)."""
    app = create_app()

    # TestClient triggers lifespan events on enter/exit
    with TestClient(app, base_url="http://test") as client:
        response = client.get("/health")
        assert response.status_code == status.HTTP_200_OK
