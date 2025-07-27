"""
Test cases for Area API endpoints
"""
from typing import Any

import pytest # type: ignore
from fastapi.testclient import TestClient


class TestAreaAPI:
    """Test class for area-related endpoints."""

    def test_create_area_success(self, client: TestClient) -> None:
        """Test creating new area successfully."""
        area_data: dict[str, str] = {"name": "Software Development"}
        
        response = client.post("/api/v1/areas/", json=area_data)
        
        assert response.status_code == 201
        data: dict[str, Any] = response.json()
        assert data["success"] is True
        assert data["message"] == "Area created successfully"
        assert "data" in data
        assert data["data"]["name"] == "Software Development"
        assert "area_id" in data["data"]

    def test_create_area_invalid_data(self, client: TestClient) -> None:
        """Test creating area with invalid data."""
        invalid_data: dict[str, str] = {"invalid_field": "test"}
        
        response = client.post("/api/v1/areas/", json=invalid_data)
        
        assert response.status_code == 422

    def test_get_areas_pagination(self, client: TestClient) -> None:
        """Test getting areas with pagination."""
        # First create some areas
        for i in range(3):
            area_data: dict[str, str] = {"name": f"Test Area {i}"}
            client.post("/api/v1/areas/", json=area_data)
        
        response = client.get("/api/v1/areas/?page=1&page_size=2")
        
        assert response.status_code == 200
        data: dict[str, Any] = response.json()
        assert data["success"] is True
        assert "data" in data
        assert len(data["data"]) <= 2
        assert "pagination" in data

    def test_search_areas(self, client: TestClient) -> None:
        """Test searching areas by name."""
        # Create an area to search for
        area_data: dict[str, str] = {"name": "Marketing Department"}
        client.post("/api/v1/areas/", json=area_data)
        
        response = client.get("/api/v1/areas/search?query=Marketing")
        
        assert response.status_code == 200
        data: dict[str, Any] = response.json()
        assert data["success"] is True
        assert "data" in data

    def test_get_area_by_id_success(self, client: TestClient) -> None:
        """Test getting area by ID."""
        # First create an area
        area_data: dict[str, str] = {"name": "Human Resources"}
        create_response = client.post("/api/v1/areas/", json=area_data)
        created_area: dict[str, Any] = create_response.json()["data"]
        
        response = client.get(f"/api/v1/areas/{created_area['area_id']}")
        
        assert response.status_code == 200
        data: dict[str, Any] = response.json()
        assert data["success"] is True
        assert data["data"]["name"] == "Human Resources"
        assert data["data"]["area_id"] == created_area["area_id"]

    def test_get_area_by_id_not_found(self, client: TestClient) -> None:
        """Test getting non-existent area."""
        response = client.get("/api/v1/areas/99999")
        
        assert response.status_code == 404
        data: dict[str, Any] = response.json()
        assert "detail" in data
        assert data["detail"] == "Area not found"

    def test_update_area_success(self, client: TestClient) -> None:
        """Test updating area."""
        # First create an area
        area_data: dict[str, str] = {"name": "Area to Update"}
        create_response = client.post("/api/v1/areas/", json=area_data)
        created_area: dict[str, Any] = create_response.json()["data"]
        
        # Update the area
        update_data: dict[str, str] = {"name": "Updated Area Name"}
        response = client.put(f"/api/v1/areas/{created_area['area_id']}", json=update_data)
        
        assert response.status_code == 200
        data: dict[str, Any] = response.json()
        assert data["success"] is True
        assert data["message"] == "Area updated successfully"
        assert data["data"]["name"] == "Updated Area Name"

    def test_update_area_not_found(self, client: TestClient) -> None:
        """Test updating non-existent area."""
        update_data: dict[str, str] = {"name": "Non-existent Area"}
        response = client.put("/api/v1/areas/99999", json=update_data)
        
        assert response.status_code == 404
        data: dict[str, Any] = response.json()
        assert "detail" in data
        assert data["detail"] == "Area not found"

    def test_delete_area_success(self, client: TestClient) -> None:
        """Test deleting area."""
        # First create an area
        area_data: dict[str, str] = {"name": "Area to Delete"}
        create_response = client.post("/api/v1/areas/", json=area_data)
        created_area: dict[str, Any] = create_response.json()["data"]
        
        # Delete the area
        response = client.delete(f"/api/v1/areas/{created_area['area_id']}")
        
        assert response.status_code == 204

    def test_delete_area_not_found(self, client: TestClient) -> None:
        """Test deleting non-existent area."""
        response = client.delete("/api/v1/areas/99999")
        
        assert response.status_code == 404
        data: dict[str, Any] = response.json()
        assert "detail" in data
        assert data["detail"] == "Area not found"
