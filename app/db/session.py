from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import settings

engine: AsyncEngine | None = None


def init_db() -> None:
    """Initialize the database engine."""
    global engine  # noqa: PLW0603
    engine = create_async_engine(
        str(settings.DATABASE_URL),
        echo=False,
        future=True,
        pool_size=20,
        max_overflow=10,
        pool_pre_ping=True,
    )


async def close_db() -> None:
    """Close the database engine."""
    global engine  # noqa: PLW0603
    if engine:
        await engine.dispose()
        engine = None


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Get a new database session."""
    if not engine:
        raise RuntimeError("Database engine is not initialized")

    async_session = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
