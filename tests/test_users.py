import pytest
from fastapi.testclient import TestClient


class TestUserRegister:
    """Test user registration endpoint"""

    def test_register_user_success(self, client, test_user_data, clean_users):
        """Test successful user registration"""
        response = client.post("/api/v1/users/register", json=test_user_data)
        assert response.status_code == 201

        data = response.json()
        assert data["username"] == test_user_data["username"]
        assert data["email"] == test_user_data["email"]
        assert data["userType"] == test_user_data["userType"]
        assert data["isActive"] == test_user_data["isActive"]
        assert "_id" in data
        assert "createdAt" in data
        assert "updatedAt" in data
        assert "password" not in data  # Password should not be in response

    # def test_register_user_missing_username(self, client, clean_users):
    #     """Test registration with missing username"""
    #     response = client.post("/api/v1/users/register", json={
    #         "email": "test@example.com",
    #         "password": "password123"
    #     })
    #     assert response.status_code == 422  # Validation error

    # def test_register_user_missing_email(self, client, clean_users):
    #     """Test registration with missing email"""
    #     response = client.post("/api/v1/users/register", json={
    #         "username": "testuser",
    #         "password": "password123"
    #     })
    #     assert response.status_code == 422

    # def test_register_user_missing_password(self, client, clean_users):
    #     """Test registration with missing password"""
    #     response = client.post("/api/v1/users/register", json={
    #         "username": "testuser",
    #         "email": "test@example.com"
    #     })
    #     assert response.status_code == 422

    # def test_register_user_short_username(self, client, clean_users):
    #     """Test registration with username shorter than 3 characters"""
    #     response = client.post("/api/v1/users/register", json={
    #         "username": "ab",
    #         "email": "test@example.com",
    #         "password": "password123"
    #     })
    #     assert response.status_code == 422

    # def test_register_user_short_password(self, client, clean_users):
    #     """Test registration with password shorter than 6 characters"""
    #     response = client.post("/api/v1/users/register", json={
    #         "username": "testuser",
    #         "email": "test@example.com",
    #         "password": "12345"
    #     })
    #     assert response.status_code == 422

    # def test_register_user_invalid_email(self, client, clean_users):
    #     """Test registration with invalid email format"""
    #     response = client.post("/api/v1/users/register", json={
    #         "username": "testuser",
    #         "email": "invalid-email",
    #         "password": "password123"
    #     })
    #     assert response.status_code == 422

    # def test_register_duplicate_email(self, client, test_user_data, clean_users):
    #     """Test registration with duplicate email"""
    #     # Register first user
    #     client.post("/api/v1/users/register", json=test_user_data)

    #     # Try to register with same email
    #     response = client.post("/api/v1/users/register", json={
    #         "username": "testuser2",
    #         "email": test_user_data["email"],
    #         "password": "password123"
    #     })
    #     assert response.status_code == 400
    #     assert response.json()["detail"] == "Email already registered"

    # def test_register_duplicate_username(self, client, test_user_data, clean_users):
    #     """Test registration with duplicate username"""
    #     # Register first user
    #     client.post("/api/v1/users/register", json=test_user_data)

    #     # Try to register with same username
    #     response = client.post("/api/v1/users/register", json={
    #         "username": test_user_data["username"],
    #         "email": "another@example.com",
    #         "password": "password123"
    #     })
    #     assert response.status_code == 400
    #     assert response.json()["detail"] == "Username already taken"


# class TestUserLogin:
#     """Test user login endpoint"""

#     def test_login_success(self, client, test_user_data, clean_users):
#         """Test successful login"""
#         # Register user first
#         client.post("/api/v1/users/register", json=test_user_data)

#         # Login
#         response = client.post("/api/v1/users/login", json={
#             "username": test_user_data["username"],
#             "password": test_user_data["password"]
#         })
#         assert response.status_code == 200

#         data = response.json()
#         assert "access_token" in data
#         assert data["token_type"] == "bearer"

#     def test_login_wrong_username(self, client, test_user_data, clean_users):
#         """Test login with wrong username"""
#         # Register user first
#         client.post("/api/v1/users/register", json=test_user_data)

#         # Login with wrong username
#         response = client.post("/api/v1/users/login", json={
#             "username": "wronguser",
#             "password": test_user_data["password"]
#         })
#         assert response.status_code == 401
#         assert response.json()["detail"] == "Incorrect username or password"

#     def test_login_wrong_password(self, client, test_user_data, clean_users):
#         """Test login with wrong password"""
#         # Register user first
#         client.post("/api/v1/users/register", json=test_user_data)

#         # Login with wrong password
#         response = client.post("/api/v1/users/login", json={
#             "username": test_user_data["username"],
#             "password": "wrongpassword"
#         })
#         assert response.status_code == 401
#         assert response.json()["detail"] == "Incorrect username or password"

#     def test_login_missing_fields(self, client):
#         """Test login with missing fields"""
#         response = client.post("/api/v1/users/login", json={
#             "username": "testuser"
#         })
#         assert response.status_code == 422


# class TestGetUsers:
#     """Test getting users endpoint"""

#     def test_get_users_empty(self, client, clean_users):
#         """Test getting users when none exist"""
#         response = client.get("/api/v1/users/")
#         assert response.status_code == 200
#         assert response.json() == []

#     def test_get_users_with_data(self, client, multiple_test_users, clean_users):
#         """Test getting users with existing data"""
#         response = client.get("/api/v1/users/")
#         assert response.status_code == 200

#         users = response.json()
#         assert len(users) == 3
#         assert "username" in users[0]
#         assert "email" in users[0]
#         assert "password" not in users[0]

#     def test_get_users_with_pagination(self, client, multiple_test_users, clean_users):
#         """Test getting users with pagination"""
#         response = client.get("/api/v1/users/?skip=1&limit=2")
#         assert response.status_code == 200

#         users = response.json()
#         assert len(users) <= 2


# class TestGetUserById:
#     """Test getting a single user by ID"""

#     def test_get_user_success(self, client, test_user, clean_users):
#         """Test successfully getting a user by ID"""
#         user_id = test_user["_id"]
#         response = client.get(f"/api/v1/users/{user_id}")
#         assert response.status_code == 200

#         data = response.json()
#         assert data["_id"] == user_id
#         assert data["username"] == test_user["username"]
#         assert "password" not in data

#     def test_get_user_not_found(self, client, clean_users):
#         """Test getting a non-existent user"""
#         fake_id = "507f1f77bcf86cd799439011"
#         response = client.get(f"/api/v1/users/{fake_id}")
#         assert response.status_code == 404
#         assert response.json()["detail"] == "User not found"

#     def test_get_user_invalid_id(self, client, clean_users):
#         """Test getting a user with invalid ID"""
#         response = client.get("/api/v1/users/invalid-id")
#         assert response.status_code in [400, 404, 422]


# class TestUpdateUser:
#     """Test updating user endpoint"""

#     def test_update_user_username(self, client, test_user, clean_users):
#         """Test updating user username"""
#         user_id = test_user["_id"]
#         response = client.put(f"/api/v1/users/{user_id}", json={
#             "username": "updateduser"
#         })
#         assert response.status_code == 200

#         data = response.json()
#         assert data["username"] == "updateduser"
#         assert data["email"] == test_user["email"]

#     def test_update_user_email(self, client, test_user, clean_users):
#         """Test updating user email"""
#         user_id = test_user["_id"]
#         response = client.put(f"/api/v1/users/{user_id}", json={
#             "email": "updated@example.com"
#         })
#         assert response.status_code == 200

#         data = response.json()
#         assert data["email"] == "updated@example.com"
#         assert data["username"] == test_user["username"]

#     def test_update_user_password(self, client, test_user, clean_users):
#         """Test updating user password"""
#         user_id = test_user["_id"]
#         response = client.put(f"/api/v1/users/{user_id}", json={
#             "password": "newpassword123"
#         })
#         assert response.status_code == 200

#     def test_update_user_multiple_fields(self, client, test_user, clean_users):
#         """Test updating multiple user fields"""
#         user_id = test_user["_id"]
#         response = client.put(f"/api/v1/users/{user_id}", json={
#             "username": "updateduser",
#             "email": "updated@example.com",
#             "isActive": False
#         })
#         assert response.status_code == 200

#         data = response.json()
#         assert data["username"] == "updateduser"
#         assert data["email"] == "updated@example.com"
#         assert data["isActive"] is False

#     def test_update_user_not_found(self, client, clean_users):
#         """Test updating a non-existent user"""
#         fake_id = "507f1f77bcf86cd799439011"
#         response = client.put(f"/api/v1/users/{fake_id}", json={
#             "username": "updateduser"
#         })
#         assert response.status_code == 404
#         assert response.json()["detail"] == "User not found"

#     def test_update_user_duplicate_email(self, client, test_user_data, clean_users):
#         """Test updating user with duplicate email"""
#         # Register two users
#         response1 = client.post("/api/v1/users/register", json=test_user_data)
#         user1 = response1.json()

#         response2 = client.post("/api/v1/users/register", json={
#             "username": "user2",
#             "email": "user2@example.com",
#             "password": "password123"
#         })
#         user2 = response2.json()

#         # Try to update user2's email to user1's email
#         response = client.put(f"/api/v1/users/{user2['_id']}", json={
#             "email": user1["email"]
#         })
#         assert response.status_code == 400
#         assert response.json()["detail"] == "Email already registered"

#     def test_update_user_short_password(self, client, test_user, clean_users):
#         """Test updating user with short password"""
#         user_id = test_user["_id"]
#         response = client.put(f"/api/v1/users/{user_id}", json={
#             "password": "12345"
#         })
#         assert response.status_code == 422


# class TestDeleteUser:
#     """Test deleting user endpoint"""

#     def test_delete_user_success(self, client, test_user_data, clean_users):
#         """Test successfully deleting a user"""
#         # Register user first
#         response = client.post("/api/v1/users/register", json=test_user_data)
#         user_id = response.json()["_id"]

#         # Delete user
#         response = client.delete(f"/api/v1/users/{user_id}")
#         assert response.status_code == 204

#         # Verify user is deleted
#         response = client.get(f"/api/v1/users/{user_id}")
#         assert response.status_code == 404

#     def test_delete_user_not_found(self, client, clean_users):
#         """Test deleting a non-existent user"""
#         fake_id = "507f1f77bcf86cd799439011"
#         response = client.delete(f"/api/v1/users/{fake_id}")
#         assert response.status_code == 404
#         assert response.json()["detail"] == "User not found"

#     def test_delete_user_invalid_id(self, client, clean_users):
#         """Test deleting a user with invalid ID"""
#         response = client.delete("/api/v1/users/invalid-id")
#         assert response.status_code in [400, 404, 422]


# class TestUserWorkflow:
#     """Test complete user workflows"""

#     def test_complete_user_lifecycle(self, client, clean_users):
#         """Test complete user lifecycle: register -> login -> get -> update -> delete"""
#         # 1. Register
#         user_data = {
#             "username": "lifecycleuser",
#             "email": "lifecycle@example.com",
#             "password": "password123"
#         }
#         response = client.post("/api/v1/users/register", json=user_data)
#         assert response.status_code == 201
#         user = response.json()
#         user_id = user["_id"]

#         # 2. Login
#         response = client.post("/api/v1/users/login", json={
#             "username": user_data["username"],
#             "password": user_data["password"]
#         })
#         assert response.status_code == 200
#         assert "access_token" in response.json()

#         # 3. Get user
#         response = client.get(f"/api/v1/users/{user_id}")
#         assert response.status_code == 200
#         assert response.json()["username"] == user_data["username"]

#         # 4. Update user
#         response = client.put(f"/api/v1/users/{user_id}", json={
#             "username": "updatedlifecycle"
#         })
#         assert response.status_code == 200
#         assert response.json()["username"] == "updatedlifecycle"

#         # 5. Delete user
#         response = client.delete(f"/api/v1/users/{user_id}")
#         assert response.status_code == 204

#         # 6. Verify deletion
#         response = client.get(f"/api/v1/users/{user_id}")
#         assert response.status_code == 404
