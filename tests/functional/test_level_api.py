"""
Test cases for Level API endpoints
"""
from typing import Any

from fastapi.testclient import TestClient


class TestLevelAPI:
    """Test class for level-related endpoints."""

    def test_create_level_success(self, client: TestClient) -> None:
        """Test creating new level successfully."""
        level_data: dict[str, str] = {"name": "Senior Level"}
        
        response = client.post("/api/v1/levels/", json=level_data)
        
        assert response.status_code == 201
        data: dict[str, Any] = response.json()
        assert data["success"] is True
        assert data["message"] == "Level created successfully"
        assert "data" in data
        assert data["data"]["name"] == "Senior Level"
        assert "level_id" in data["data"]

    def test_create_level_invalid_data(self, client: TestClient) -> None:
        """Test creating level with invalid data."""
        invalid_data: dict[str, str] = {"invalid_field": "test"}
        
        response = client.post("/api/v1/levels/", json=invalid_data)
        
        assert response.status_code == 422

    def test_get_levels_pagination(self, client: TestClient) -> None:
        """Test getting levels with pagination."""
        # First create some levels
        for i in range(3):
            level_data: dict[str, str] = {"name": f"Test Level {i}"}
            client.post("/api/v1/levels/", json=level_data)
        
        response = client.get("/api/v1/levels/?page=1&page_size=2")
        
        assert response.status_code == 200
        data: dict[str, Any] = response.json()
        assert data["success"] is True
        assert "data" in data
        assert len(data["data"]) <= 2
        assert "pagination" in data

    def test_search_levels(self, client: TestClient) -> None:
        """Test searching levels by name."""
        # Create a level to search for
        level_data: dict[str, str] = {"name": "Junior Developer"}
        client.post("/api/v1/levels/", json=level_data)
        
        response = client.get("/api/v1/levels/search?query=Junior")
        
        assert response.status_code == 200
        data: dict[str, Any] = response.json()
        assert data["success"] is True
        assert "data" in data

    def test_get_level_by_id_success(self, client: TestClient) -> None:
        """Test getting level by ID."""
        # First create a level
        level_data: dict[str, str] = {"name": "Mid Level"}
        create_response = client.post("/api/v1/levels/", json=level_data)
        created_level: dict[str, Any] = create_response.json()["data"]
        
        response = client.get(f"/api/v1/levels/{created_level['level_id']}")
        
        assert response.status_code == 200
        data: dict[str, Any] = response.json()
        assert data["success"] is True
        assert data["data"]["name"] == "Mid Level"
        assert data["data"]["level_id"] == created_level["level_id"]

    def test_get_level_by_id_not_found(self, client: TestClient) -> None:
        """Test getting non-existent level."""
        response = client.get("/api/v1/levels/99999")
        
        assert response.status_code == 404
        data: dict[str, Any] = response.json()
        assert "detail" in data
        assert data["detail"] == "Level not found"

    def test_update_level_success(self, client: TestClient) -> None:
        """Test updating level."""
        # First create a level
        level_data: dict[str, str] = {"name": "Level to Update"}
        create_response = client.post("/api/v1/levels/", json=level_data)
        created_level: dict[str, Any] = create_response.json()["data"]
        
        # Update the level
        update_data: dict[str, str] = {"name": "Updated Level Name"}
        response = client.put(f"/api/v1/levels/{created_level['level_id']}", json=update_data)
        
        assert response.status_code == 200
        data: dict[str, Any] = response.json()
        assert data["success"] is True
        assert data["message"] == "Level updated successfully"
        assert data["data"]["name"] == "Updated Level Name"

    def test_update_level_not_found(self, client: TestClient) -> None:
        """Test updating non-existent level."""
        update_data: dict[str, str] = {"name": "Non-existent Level"}
        response = client.put("/api/v1/levels/99999", json=update_data)
        
        assert response.status_code == 404
        data: dict[str, Any] = response.json()
        assert "detail" in data
        assert data["detail"] == "Level not found"

    def test_delete_level_success(self, client: TestClient) -> None:
        """Test deleting level."""
        # First create a level
        level_data: dict[str, str] = {"name": "Level to Delete"}
        create_response = client.post("/api/v1/levels/", json=level_data)
        created_level: dict[str, Any] = create_response.json()["data"]
        
        # Delete the level
        response = client.delete(f"/api/v1/levels/{created_level['level_id']}")
        
        assert response.status_code == 204

    def test_delete_level_not_found(self, client: TestClient) -> None:
        """Test deleting non-existent level."""
        response = client.delete("/api/v1/levels/99999")
        
        assert response.status_code == 404
        data: dict[str, Any] = response.json()
        assert "detail" in data
        assert data["detail"] == "Level not found"
