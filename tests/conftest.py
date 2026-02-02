import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import db


@pytest.fixture(autouse=True)
def setup_database():
    """Setup database connection for each test"""
    # Connect to MongoDB before each test
    db.connect()
    yield
    # Cleanup after each test
    db.close()


@pytest.fixture
def client():
    """Create a test client"""
    return TestClient(app)


@pytest.fixture
def clean_users(client):
    """Clean up users after test"""
    yield
    # Get all users and delete them
    response = client.get("/api/v1/users/")
    if response.status_code == 200:
        users = response.json()
        for user in users:
            client.delete(f"/api/v1/users/{user['_id']}")


@pytest.fixture
def test_user_data():
    """Test user data"""
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "123456",  # Short password to avoid bcrypt 72 byte limit
        "userType": "user",
        "isActive": True
    }


@pytest.fixture
def test_user(client, test_user_data):
    """Create a test user and return it"""
    response = client.post("/api/v1/users/register", json=test_user_data)
    if response.status_code == 201:
        return response.json()
    return None


@pytest.fixture
def multiple_test_users(client):
    """Create multiple test users"""
    users_data = [
        {
            "username": f"user{i}",
            "email": f"user{i}@example.com",
            "password": "test123",
            "userType": "user",
            "isActive": True
        }
        for i in range(1, 4)
    ]
    created_users = []
    for user_data in users_data:
        response = client.post("/api/v1/users/register", json=user_data)
        if response.status_code == 201:
            created_users.append(response.json())
    return created_users
