from unittest.mock import Mock

import pytest
from sqlmodel import select

from app.db.session import create_db_engine, get_session
from app.main import app as fastapi_app
from app.modules.user.models import User


@pytest.mark.asyncio
async def test_get_session():
    """Test the get_session dependency directly to ensure coverage."""
    # Create a mock request with app.state.engine
    mock_request = Mock()
    mock_request.app.state = fastapi_app.state

    async for session in get_session(mock_request):
        assert session is not None
        # Verify it works by executing a simple query
        await session.exec(select(User).limit(1))


@pytest.mark.asyncio
async def test_db_lifecycle_and_error_handling():
    """Test database initialization, closing, and error handling."""
    # 1. Close the DB (simulating shutdown or uninitialized state)
    if fastapi_app.state.engine:
        await fastapi_app.state.engine.dispose()
        fastapi_app.state.engine = None
    assert fastapi_app.state.engine is None

    # 2. Verify closing is idempotent (safe when already closed)
    # (No-op since we're using app.state now)

    # 3. Verify get_session raises RuntimeError when engine is None
    mock_request = Mock()
    mock_request.app.state.engine = None
    with pytest.raises(
        RuntimeError, match="Database engine is not initialized"
    ):
        async for _ in get_session(mock_request):
            pass

    # 4. Re-initialize the DB (restore state for other tests/teardown)
    fastapi_app.state.engine = create_db_engine()
    assert fastapi_app.state.engine is not None
