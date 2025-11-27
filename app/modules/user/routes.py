import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.openapi import APITag
from app.db.session import get_session
from app.modules.user.models import User
from app.modules.user.repository import UserRepository
from app.modules.user.schemas import UserCreate, UserRead, UserUpdate
from app.modules.user.service import UserService

router = APIRouter(prefix="/users", tags=[APITag.users])


def get_user_service(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> UserService:
    """Get the user service."""
    repository = UserRepository(session)
    return UserService(repository)


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_create: UserCreate,
    service: Annotated[UserService, Depends(get_user_service)],
) -> User:
    """Create a new user."""
    return await service.create_user(user_create)


@router.get("/", response_model=list[UserRead])
async def list_users(
    service: Annotated[UserService, Depends(get_user_service)],
    skip: int = 0,
    limit: int = 100,
) -> list[User]:
    """List users."""
    return await service.list_users(skip, limit)


@router.get("/{user_id}", response_model=UserRead)
async def get_user(
    user_id: uuid.UUID,
    service: Annotated[UserService, Depends(get_user_service)],
) -> User:
    """Get a user by ID."""
    return await service.get_user(user_id)


@router.patch("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: uuid.UUID,
    user_update: UserUpdate,
    service: Annotated[UserService, Depends(get_user_service)],
) -> User:
    """Update a user."""
    return await service.update_user(user_id, user_update)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: uuid.UUID,
    service: Annotated[UserService, Depends(get_user_service)],
) -> None:
    """Delete a user."""
    await service.delete_user(user_id)
