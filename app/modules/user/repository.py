import uuid

from sqlalchemy import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.modules.user.models import User
from app.modules.user.schemas import UserCreate, UserUpdate


class UserRepository:
    """Repository for User operations."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize the repository."""
        self.session = session

    async def create(self, user_create: UserCreate) -> User:
        """Create a new user."""
        db_user = User.model_validate(user_create)
        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)
        return db_user

    async def get(self, user_id: uuid.UUID) -> User | None:
        """Get a user by ID."""
        return await self.session.get(User, user_id)

    async def get_by_email(self, email: str) -> User | None:
        """Get a user by email."""
        statement = select(User).where(User.email == email)  # type: ignore
        result = await self.session.exec(statement)  # type: ignore
        return result.scalars().first()

    async def list(self, skip: int = 0, limit: int = 100) -> list[User]:
        """List users."""
        statement = select(User).offset(skip).limit(limit)
        result = await self.session.exec(statement)  # type: ignore
        return list(result.scalars().all())

    async def update(self, user: User, user_update: UserUpdate) -> User:
        """Update a user."""
        user_data = user_update.model_dump(exclude_unset=True)
        for key, value in user_data.items():
            setattr(user, key, value)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def delete(self, user: User) -> None:
        """Delete a user."""
        await self.session.delete(user)
        await self.session.commit()
