"""
Functional tests for Authentication API endpoints.
Tests registration, login, and user profile endpoints.
"""
import pytest # type: ignore
from typing import Any
from fastapi.testclient import TestClient

class TestAuthAPI:
    """Test suite for Authentication API endpoints."""
    
    def test_register_headhunter_success(self, client: TestClient) -> None:
        """Test successful headhunter registration."""
        headhunter_data: dict[str, Any] = {
            "name": "Test Headhunter",
            "phone": "1234567890",
            "email": "test@headhunter.com",
            "area_id": 1,
            "role": "headhunter",
            "password": "securepassword123"
        }
        
        response = client.post("/api/v1/auth/register", json=headhunter_data)
        
        assert response.status_code == 201
        data: dict[str, Any] = response.json()  # type: ignore
        assert data["success"] is True
        assert data["message"] == "Headhunter registered successfully"
        assert "data" in data
        assert "headhunter_id" in data["data"]

    def test_register_headhunter_invalid_email(self, client: TestClient) -> None:
        """Test registration with invalid email format."""
        headhunter_data: dict[str, Any] = {
            "name": "Test Headhunter",
            "phone": "1234567890",
            "email": "invalid-email",  # Invalid email format
            "area_id": 1,
            "password": "securepassword123"
        }
        
        response = client.post("/api/v1/auth/register", json=headhunter_data)
        
        assert response.status_code == 422  # Validation error

    def test_register_headhunter_weak_password(self, client: TestClient) -> None:
        """Test registration with weak password."""
        headhunter_data: dict[str, Any] = {
            "name": "Test Headhunter",
            "phone": "1234567890",
            "email": "weak@test.com",
            "area_id": 1,
            "password": "123"  # Too weak password
        }
        
        response = client.post("/api/v1/auth/register", json=headhunter_data)
        
        assert response.status_code == 422  # Validation error

    def test_register_headhunter_missing_fields(self, client: TestClient) -> None:
        """Test registration with missing required fields."""
        headhunter_data: dict[str, Any] = {
            "name": "Test Headhunter",
            # Missing email, phone, area_id, password
        }
        
        response = client.post("/api/v1/auth/register", json=headhunter_data)
        
        assert response.status_code == 422  # Validation error

    def test_login_success(self, client: TestClient) -> None:
        """Test successful login."""
        # First register a headhunter
        headhunter_data: dict[str, Any] = {
            "name": "Login Test User",
            "phone": "1234567890",
            "email": "login@test.com",
            "area_id": 1,
            "password": "loginpassword123"
        }
        client.post("/api/v1/auth/register", json=headhunter_data)
        
        # Then try to login
        login_data: dict[str, str] = {
            "username": "login@test.com",
            "password": "loginpassword123"
        }
        
        response = client.post("/api/v1/auth/login", data=login_data)
        
        assert response.status_code == 200
        data: dict[str, Any] = response.json()  # type: ignore
        assert data["success"] is True
        assert "data" in data
        assert "access_token" in data["data"]
        assert data["data"]["token_type"] == "bearer"

    def test_login_invalid_credentials(self, client: TestClient) -> None:
        """Test login with invalid credentials."""
        login_data: dict[str, str] = {
            "username": "nonexistent@test.com",
            "password": "wrongpassword"
        }
        
        response = client.post("/api/v1/auth/login", data=login_data)
        
        assert response.status_code in [401, 404]  # Unauthorized or Not Found

    def test_login_missing_credentials(self, client: TestClient) -> None:
        """Test login without providing credentials."""
        response = client.post("/api/v1/auth/login", data={})
        
        assert response.status_code == 422  # Validation error

    def test_get_current_user_success(self, client: TestClient) -> None:
        """Test getting current user profile with valid token."""
        # First register and login to get a token
        headhunter_data: dict[str, Any] = {
            "name": "Profile Test User",
            "phone": "1234567890",
            "email": "profile@test.com",
            "area_id": 1,
            "password": "profilepassword123"
        }
        client.post("/api/v1/auth/register", json=headhunter_data)
        
        login_data: dict[str, str] = {
            "username": "profile@test.com",
            "password": "profilepassword123"
        }
        login_response = client.post("/api/v1/auth/login", data=login_data)
        token: str = login_response.json()["data"]["access_token"]  # type: ignore
        
        # Test getting current user profile
        headers: dict[str, str] = {"Authorization": f"Bearer {token}"}
        response = client.get("/api/v1/auth/me", headers=headers)
        
        assert response.status_code == 200
        data: dict[str, Any] = response.json()  # type: ignore
        assert data["success"] is True
        assert "data" in data
        assert data["data"]["email"] == "profile@test.com"

    def test_get_current_user_invalid_token(self, client: TestClient) -> None:
        """Test getting current user with invalid token."""
        headers: dict[str, str] = {"Authorization": "Bearer invalid_token"}
        response = client.get("/api/v1/auth/me", headers=headers)
        
        assert response.status_code == 401  # Unauthorized

    def test_get_current_user_no_token(self, client: TestClient) -> None:
        """Test getting current user without token."""
        response = client.get("/api/v1/auth/me")
        
        assert response.status_code == 401  # Unauthorized

class TestAuthAPIValidation:
    """Additional validation tests for authentication endpoints."""

    def test_register_phone_validation(self, client: TestClient) -> None:
        """Test phone number validation."""
        headhunter_data: dict[str, Any] = {
            "name": "Test Headhunter",
            "phone": "123",  # Too short (less than 10 characters)
            "email": "phone@test.com",
            "area_id": 1,
            "password": "testpassword123"
        }
        
        response = client.post("/api/v1/auth/register", json=headhunter_data)
        
        assert response.status_code == 422  # Validation error

    def test_register_area_id_validation(self, client: TestClient) -> None:
        """Test area_id validation."""
        headhunter_data: dict[str, Any] = {
            "name": "Test Headhunter",
            "phone": "1234567890",
            "email": "area@test.com",
            "area_id": "invalid_area_id",  # Should be integer
            "password": "testpassword123"
        }
        
        response = client.post("/api/v1/auth/register", json=headhunter_data)
        
        assert response.status_code == 422  # Validation error

    def test_register_name_length_validation(self, client: TestClient) -> None:
        """Test name length validation."""
        headhunter_data: dict[str, Any] = {
            "name": "",  # Empty name
            "phone": "1234567890",
            "email": "name@test.com",
            "area_id": 1,
            "password": "testpassword123"
        }
        
        response = client.post("/api/v1/auth/register", json=headhunter_data)
        
        assert response.status_code == 422  # Validation error
