import pytest
from sqlmodel import select

import app.db.session
from app.db.session import get_session
from app.modules.user.models import User


@pytest.mark.asyncio
async def test_get_session():
    """Test the get_session dependency directly to ensure coverage."""
    async for session in get_session():
        assert session is not None
        # Verify it works by executing a simple query
        await session.exec(select(User).limit(1))


@pytest.mark.asyncio
async def test_db_lifecycle_and_error_handling():
    """Test database initialization, closing, and error handling."""
    # 1. Close the DB (simulating shutdown or uninitialized state)
    await app.db.session.close_db()
    assert app.db.session.engine is None

    # 2. Verify close_db is idempotent (safe to call when already closed)
    await app.db.session.close_db()
    assert app.db.session.engine is None

    # 3. Verify get_session raises RuntimeError when engine is None
    with pytest.raises(RuntimeError, match="Database engine is not initialized"):
        async for _ in get_session():
            pass

    # 4. Re-initialize the DB (restore state for other tests/teardown)
    app.db.session.init_db()
    assert app.db.session.engine is not None
