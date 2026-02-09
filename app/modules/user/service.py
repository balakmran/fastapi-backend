import uuid

from fastapi import HTTPException, status

from app.modules.user.models import User
from app.modules.user.repository import UserRepository
from app.modules.user.schemas import UserCreate, UserUpdate


class UserService:
    """Service for User operations."""

    def __init__(self, repository: UserRepository) -> None:
        """Initialize the service."""
        self.repository = repository

    async def create_user(self, user_create: UserCreate) -> User:
        """Create a new user."""
        existing_user = await self.repository.get_by_email(user_create.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        return await self.repository.create(user_create)

    async def get_user(self, user_id: uuid.UUID) -> User:
        """Get a user by ID."""
        user = await self.repository.get(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return user

    async def list_users(self, skip: int = 0, limit: int = 100) -> list[User]:
        """List users."""
        return await self.repository.list(skip, limit)

    async def update_user(
        self, user_id: uuid.UUID, user_update: UserUpdate
    ) -> User:
        """Update a user."""
        user = await self.get_user(user_id)
        return await self.repository.update(user, user_update)

    async def delete_user(self, user_id: uuid.UUID) -> None:
        """Delete a user."""
        user = await self.get_user(user_id)
        await self.repository.delete(user)
