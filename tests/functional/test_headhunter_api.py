"""
Test cases for Headhunter API endpoints
"""
from typing import Any

from fastapi.testclient import TestClient


class TestHeadhunterAPI:
    """Test class for headhunter-related endpoints."""

    def test_create_headhunter_success(self, client: TestClient) -> None:
        """Test creating new headhunter successfully."""
        headhunter_data: dict[str, Any] = {
            "name": "John Doe",
            "phone": "1234567890",
            "email": "john.doe@headhunter.com",
            "area_id": 1,
            "role": "headhunter",
            "password": "securepassword123"
        }
        
        response = client.post("/api/v1/headhunters/", json=headhunter_data)
        
        assert response.status_code == 201
        data: dict[str, Any] = response.json()
        assert data["success"] is True
        assert data["message"] == "Headhunter created successfully"
        assert "data" in data
        assert data["data"]["name"] == "John Doe"
        assert data["data"]["email"] == "john.doe@headhunter.com"
        assert "headhunter_id" in data["data"]
        # Password should not be in response
        assert "password" not in data["data"]
        assert "hashed_password" not in data["data"]

    def test_create_headhunter_invalid_data(self, client: TestClient) -> None:
        """Test creating headhunter with invalid data."""
        invalid_data: dict[str, str] = {"invalid_field": "test"}
        
        response = client.post("/api/v1/headhunters/", json=invalid_data)
        
        assert response.status_code == 422

    def test_create_headhunter_invalid_email(self, client: TestClient) -> None:
        """Test creating headhunter with invalid email."""
        headhunter_data: dict[str, Any] = {
            "name": "Test User",
            "phone": "1234567890",
            "email": "invalid-email",
            "area_id": 1,
            "password": "securepassword123"
        }
        
        response = client.post("/api/v1/headhunters/", json=headhunter_data)
        
        assert response.status_code == 422

    def test_get_headhunters_pagination(self, client: TestClient) -> None:
        """Test getting headhunters with pagination."""
        # First create some headhunters
        for i in range(3):
            headhunter_data: dict[str, Any] = {
                "name": f"Test Headhunter {i}",
                "phone": f"123456789{i}",
                "email": f"test{i}@headhunter.com",
                "area_id": 1,
                "password": "testpassword123"
            }
            client.post("/api/v1/headhunters/", json=headhunter_data)
        
        response = client.get("/api/v1/headhunters/?page=1&page_size=2")
        
        assert response.status_code == 200
        data: dict[str, Any] = response.json()
        assert data["success"] is True
        assert "data" in data
        assert len(data["data"]) <= 2
        assert "pagination" in data

    def test_search_headhunters(self, client: TestClient) -> None:
        """Test searching headhunters by name."""
        # Create a headhunter to search for
        headhunter_data: dict[str, Any] = {
            "name": "Searchable Headhunter",
            "phone": "1234567890",
            "email": "searchable@headhunter.com",
            "area_id": 1,
            "password": "testpassword123"
        }
        client.post("/api/v1/headhunters/", json=headhunter_data)
        
        response = client.get("/api/v1/headhunters/search?query=Searchable")
        
        assert response.status_code == 200
        data: dict[str, Any] = response.json()
        assert data["success"] is True
        assert "data" in data

    def test_get_headhunter_by_id_success(self, client: TestClient) -> None:
        """Test getting headhunter by ID."""
        # First create a headhunter
        headhunter_data: dict[str, Any] = {
            "name": "Get Test Headhunter",
            "phone": "1234567890",
            "email": "gettest@headhunter.com",
            "area_id": 1,
            "password": "testpassword123"
        }
        create_response = client.post("/api/v1/headhunters/", json=headhunter_data)
        created_headhunter: dict[str, Any] = create_response.json()["data"]
        
        response = client.get(f"/api/v1/headhunters/{created_headhunter['headhunter_id']}")
        
        assert response.status_code == 200
        data: dict[str, Any] = response.json()
        assert data["success"] is True
        assert data["data"]["name"] == "Get Test Headhunter"
        assert data["data"]["headhunter_id"] == created_headhunter["headhunter_id"]

    def test_get_headhunter_by_id_not_found(self, client: TestClient) -> None:
        """Test getting non-existent headhunter."""
        response = client.get("/api/v1/headhunters/99999")
        
        assert response.status_code == 404
        data: dict[str, Any] = response.json()
        assert "detail" in data
        assert data["detail"] == "Headhunter not found"

    def test_update_headhunter_success(self, client: TestClient) -> None:
        """Test updating headhunter."""
        # First create a headhunter
        headhunter_data: dict[str, Any] = {
            "name": "Headhunter to Update",
            "phone": "1234567890",
            "email": "update@headhunter.com",
            "area_id": 1,
            "password": "testpassword123"
        }
        create_response = client.post("/api/v1/headhunters/", json=headhunter_data)
        created_headhunter: dict[str, Any] = create_response.json()["data"]
        
        # Update the headhunter
        update_data: dict[str, str] = {"name": "Updated Headhunter Name"}
        response = client.put(f"/api/v1/headhunters/{created_headhunter['headhunter_id']}", json=update_data)
        
        assert response.status_code == 200
        data: dict[str, Any] = response.json()
        assert data["success"] is True
        assert data["message"] == "Headhunter updated successfully"
        assert data["data"]["name"] == "Updated Headhunter Name"

    def test_update_headhunter_not_found(self, client: TestClient) -> None:
        """Test updating non-existent headhunter."""
        update_data: dict[str, str] = {"name": "Non-existent Headhunter"}
        response = client.put("/api/v1/headhunters/99999", json=update_data)
        
        assert response.status_code == 404
        data: dict[str, Any] = response.json()
        assert "detail" in data
        assert data["detail"] == "Headhunter not found"

    def test_delete_headhunter_success(self, client: TestClient) -> None:
        """Test deleting headhunter."""
        # First create a headhunter
        headhunter_data: dict[str, Any] = {
            "name": "Headhunter to Delete",
            "phone": "1234567890",
            "email": "delete@headhunter.com",
            "area_id": 1,
            "password": "testpassword123"
        }
        create_response = client.post("/api/v1/headhunters/", json=headhunter_data)
        created_headhunter: dict[str, Any] = create_response.json()["data"]
        
        # Delete the headhunter
        response = client.delete(f"/api/v1/headhunters/{created_headhunter['headhunter_id']}")
        
        assert response.status_code == 204

    def test_delete_headhunter_not_found(self, client: TestClient) -> None:
        """Test deleting non-existent headhunter."""
        response = client.delete("/api/v1/headhunters/99999")
        
        assert response.status_code == 404
        data: dict[str, Any] = response.json()
        assert "detail" in data
        assert data["detail"] == "Headhunter not found"
