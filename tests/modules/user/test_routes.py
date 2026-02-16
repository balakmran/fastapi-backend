import uuid

import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):
    """Test creating a new user."""
    response = await client.post(
        "/users/",
        json={
            "email": "test@example.com",
            "full_name": "Test User",
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["full_name"] == "Test User"
    assert "id" in data
    assert "created_at" in data


@pytest.mark.asyncio
async def test_create_user_duplicate_email(client: AsyncClient):
    """Test creating a user with a duplicate email."""
    # Create first user
    await client.post(
        "/users/",
        json={"email": "duplicate@example.com", "full_name": "First User"},
    )

    # Try to create second user with same email
    response = await client.post(
        "/users/",
        json={"email": "duplicate@example.com", "full_name": "Second User"},
    )
    assert response.status_code == status.HTTP_409_CONFLICT
    assert "Email already registered" in response.json()["detail"]


@pytest.mark.asyncio
async def test_list_users(client: AsyncClient):
    """Test listing users."""
    # Create a user to ensure list is not empty
    await client.post(
        "/users/",
        json={"email": "list@example.com", "full_name": "List User"},
    )

    response = await client.get("/users/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

    # Verify structure of first item
    user = data[0]
    assert "email" in user
    assert "id" in user


@pytest.mark.asyncio
async def test_get_user(client: AsyncClient):
    """Test getting a user by ID."""
    # Create a user
    create_res = await client.post(
        "/users/",
        json={"email": "get@example.com", "full_name": "Get User"},
    )
    user_id = create_res.json()["id"]

    # Get the user
    response = await client.get(f"/users/{user_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == "get@example.com"
    assert data["id"] == user_id


@pytest.mark.asyncio
async def test_get_user_not_found(client: AsyncClient):
    """Test getting a non-existent user."""
    random_id = uuid.uuid4()
    response = await client.get(f"/users/{random_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_update_user(client: AsyncClient):
    """Test updating a user."""
    # Create a user
    create_res = await client.post(
        "/users/",
        json={"email": "update@example.com", "full_name": "Original Name"},
    )
    user_id = create_res.json()["id"]

    # Update the user
    response = await client.patch(
        f"/users/{user_id}",
        json={"full_name": "Updated Name"},
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["full_name"] == "Updated Name"
    assert data["email"] == "update@example.com"  # Should remain unchanged


@pytest.mark.asyncio
async def test_delete_user(client: AsyncClient):
    """Test deleting a user."""
    # Create a user
    create_res = await client.post(
        "/users/",
        json={"email": "delete@example.com", "full_name": "Delete Me"},
    )
    user_id = create_res.json()["id"]

    # Delete the user
    response = await client.delete(f"/users/{user_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.content == b""  # 204 has no content

    # Verify user is gone
    get_res = await client.get(f"/users/{user_id}")
    assert get_res.status_code == status.HTTP_404_NOT_FOUND
