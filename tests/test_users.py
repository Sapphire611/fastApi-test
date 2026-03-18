import pytest
import time
import random
import string
from httpx import AsyncClient
from app.core.config import settings


def generate_unique_user_data():
    """Generate unique user data to avoid conflicts"""
    timestamp = int(time.time() * 1000)
    random_str = ''.join(random.choices(string.ascii_lowercase, k=5))
    return {
        "username": f"testuser_{timestamp}_{random_str}",
        "email": f"test_{timestamp}_{random_str}@example.com",
        "password": "test123",
        "user_type": "user",
        "is_active": True
    }


@pytest.mark.asyncio
async def test_register_user_success(client):
    """Test successful user registration"""
    user_data = generate_unique_user_data()
    response = await client.post(f"{settings.API_V1_STR}/users/register", json=user_data)
    assert response.status_code == 201

    data = response.json()
    assert data["username"] == user_data["username"]
    assert data["email"] == user_data["email"]
    assert data["user_type"] == user_data["user_type"]
    assert data["is_active"] == user_data["is_active"]
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data
    assert "password" not in data  # Password should not be in response


@pytest.mark.asyncio
async def test_register_user_missing_username(client):
    """Test registration with missing username"""
    response = await client.post(f"{settings.API_V1_STR}/users/register", json={
        "email": "test@example.com",
        "password": "test123"
    })
    assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_register_user_missing_email(client):
    """Test registration with missing email"""
    response = await client.post(f"{settings.API_V1_STR}/users/register", json={
        "username": "testuser",
        "password": "test123"
    })
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_register_user_missing_password(client):
    """Test registration with missing password"""
    response = await client.post(f"{settings.API_V1_STR}/users/register", json={
        "username": "testuser",
        "email": "test@example.com"
    })
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_register_user_short_password(client):
    """Test registration with password shorter than 6 characters"""
    response = await client.post(f"{settings.API_V1_STR}/users/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "12345"
    })
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_register_user_invalid_email(client):
    """Test registration with invalid email format"""
    response = await client.post(f"{settings.API_V1_STR}/users/register", json={
        "username": "testuser",
        "email": "invalid-email",
        "password": "test123"
    })
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_users_empty(client):
    """Test getting users endpoint"""
    response = await client.get(f"{settings.API_V1_STR}/users/")
    assert response.status_code == 200
    # Just check that we get a valid response
    users = response.json()
    assert isinstance(users, list)


@pytest.mark.asyncio
async def test_get_users_with_data(client):
    """Test getting users with existing data"""
    user_data = generate_unique_user_data()
    # Create a user first
    await client.post(f"{settings.API_V1_STR}/users/register", json=user_data)

    response = await client.get(f"{settings.API_V1_STR}/users/")
    assert response.status_code == 200

    users = response.json()
    assert len(users) >= 1
    assert "username" in users[0]
    assert "email" in users[0]
    assert "password" not in users[0]


@pytest.mark.asyncio
async def test_get_user_success(client):
    """Test successfully getting a user by ID"""
    user_data = generate_unique_user_data()
    # Create a user first
    response = await client.post(f"{settings.API_V1_STR}/users/register", json=user_data)
    user_id = response.json()["id"]

    response = await client.get(f"{settings.API_V1_STR}/users/{user_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == user_id
    assert data["username"] == user_data["username"]
    assert "password" not in data


@pytest.mark.asyncio
async def test_get_user_not_found(client):
    """Test getting a non-existent user"""
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = await client.get(f"{settings.API_V1_STR}/users/{fake_id}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_user_username(client):
    """Test updating user username"""
    user_data = generate_unique_user_data()
    # Create a user first
    response = await client.post(f"{settings.API_V1_STR}/users/register", json=user_data)
    user_id = response.json()["id"]

    new_username = f"updated_{int(time.time() * 1000)}"
    response = await client.put(f"{settings.API_V1_STR}/users/{user_id}", json={
        "username": new_username
    })
    assert response.status_code == 200

    data = response.json()
    assert data["username"] == new_username
    assert data["email"] == user_data["email"]


@pytest.mark.asyncio
async def test_update_user_not_found(client):
    """Test updating a non-existent user"""
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = await client.put(f"{settings.API_V1_STR}/users/{fake_id}", json={
        "username": "updateduser"
    })
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_user_success(client):
    """Test successfully deleting a user"""
    user_data = generate_unique_user_data()
    # Create a user first
    response = await client.post(f"{settings.API_V1_STR}/users/register", json=user_data)
    user_id = response.json()["id"]

    # Delete user
    response = await client.delete(f"{settings.API_V1_STR}/users/{user_id}")
    assert response.status_code == 204

    # Verify user is deleted
    response = await client.get(f"{settings.API_V1_STR}/users/{user_id}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_user_not_found(client):
    """Test deleting a non-existent user"""
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = await client.delete(f"{settings.API_V1_STR}/users/{fake_id}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_complete_user_lifecycle(client):
    """Test complete user lifecycle: register -> get -> update -> delete"""
    # 1. Register
    user_data = generate_unique_user_data()
    response = await client.post(f"{settings.API_V1_STR}/users/register", json=user_data)
    assert response.status_code == 201
    user = response.json()
    user_id = user["id"]

    # 2. Get user
    response = await client.get(f"{settings.API_V1_STR}/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["username"] == user_data["username"]

    # 3. Update user
    new_username = f"lifecycle_updated_{int(time.time() * 1000)}"
    response = await client.put(f"{settings.API_V1_STR}/users/{user_id}", json={
        "username": new_username
    })
    assert response.status_code == 200
    assert response.json()["username"] == new_username

    # 4. Delete user
    response = await client.delete(f"{settings.API_V1_STR}/users/{user_id}")
    assert response.status_code == 204

    # 5. Verify deletion
    response = await client.get(f"{settings.API_V1_STR}/users/{user_id}")
    assert response.status_code == 404