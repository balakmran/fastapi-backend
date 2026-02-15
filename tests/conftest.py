from collections.abc import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

import app.db.session
from app.core.config import settings
from app.db.session import close_db, get_session, init_db
from app.main import app as fastapi_app


@pytest.fixture(scope="function", autouse=True)
async def initialize_db() -> AsyncGenerator[None, None]:
    """Initialize the database engine for the test session."""
    settings.POSTGRES_DB = "postgres"
    init_db()

    # Create tables
    if app.db.session.engine:
        async with app.db.session.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

    yield

    # Drop tables (optional, but good for cleanup)
    if app.db.session.engine:
        async with app.db.session.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.drop_all)

    await close_db()


@pytest.fixture
async def db_session(initialize_db: None) -> AsyncGenerator[AsyncSession, None]:
    """Fixture that returns a SQLAlchemy session with a SAVEPOINT.

    The rollback happens after the test completes. This guarantees that the
    database is cleaned up after each test.
    """
    if not app.db.session.engine:
        raise RuntimeError("Database engine is not initialized")

    connection = await app.db.session.engine.connect()
    trans = await connection.begin()

    # Create a session bound to the connection
    session_maker = async_sessionmaker(
        bind=connection,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    session = session_maker()

    try:
        yield session
    finally:
        await session.close()
        await trans.rollback()
        await connection.close()


@pytest.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Fixture that returns an HTTP client for the application.

    It overrides the get_session dependency to use the test session.
    """
    # Override the get_session dependency to use the test session
    fastapi_app.dependency_overrides[get_session] = lambda: db_session

    async with AsyncClient(
        transport=ASGITransport(app=fastapi_app), base_url="http://test"
    ) as c:
        yield c

    # Clear overrides after test
    fastapi_app.dependency_overrides.clear()
