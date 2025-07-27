"""
Test cases for Field API endpoints
"""
from typing import Any

import pytest # type: ignore
from fastapi.testclient import TestClient


class TestFieldAPI:
    """Test class for field-related endpoints."""

    def test_create_field_success(self, client: TestClient) -> None:
        """Test creating new field successfully."""
        field_data: dict[str, str] = {"name": "Information Technology"}
        
        response = client.post("/api/v1/fields/", json=field_data)
        
        # Debug: print response details if not successful
        if response.status_code != 201:
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
        
        assert response.status_code == 201
        data: dict[str, Any] = response.json()
        assert data["success"] is True
        assert data["message"] == "Field created successfully"
        assert "data" in data
        assert data["data"]["name"] == "Information Technology"
        assert "field_id" in data["data"]

    def test_create_field_invalid_data(self, client: TestClient) -> None:
        """Test creating field with invalid data."""
        invalid_data: dict[str, str] = {"invalid_field": "test"}
        
        response = client.post("/api/v1/fields/", json=invalid_data)
        
        assert response.status_code == 422

    def test_get_fields_pagination(self, client: TestClient) -> None:
        """Test getting fields with pagination."""
        # First create some fields
        for i in range(3):
            field_data: dict[str, str] = {"name": f"Test Field {i}"}
            client.post("/api/v1/fields/", json=field_data)
        
        response = client.get("/api/v1/fields/?page=1&page_size=2")
        
        assert response.status_code == 200
        data: dict[str, Any] = response.json()
        assert data["success"] is True
        assert "data" in data
        assert len(data["data"]) <= 2
        assert "pagination" in data

    def test_search_fields(self, client: TestClient) -> None:
        """Test searching fields by name."""
        # Create a field to search for
        field_data: dict[str, str] = {"name": "Healthcare Management"}
        client.post("/api/v1/fields/", json=field_data)
        
        response = client.get("/api/v1/fields/search?query=Healthcare")
        
        assert response.status_code == 200
        data: dict[str, Any] = response.json()
        assert data["success"] is True
        assert "data" in data

    def test_get_field_by_id_success(self, client: TestClient) -> None:
        """Test getting field by ID."""
        # First create a field
        field_data: dict[str, str] = {"name": "Financial Services"}
        create_response = client.post("/api/v1/fields/", json=field_data)
        created_field: dict[str, Any] = create_response.json()["data"]
        
        response = client.get(f"/api/v1/fields/{created_field['field_id']}")
        
        assert response.status_code == 200
        data: dict[str, Any] = response.json()
        assert data["success"] is True
        assert data["data"]["name"] == "Financial Services"
        assert data["data"]["field_id"] == created_field["field_id"]

    def test_get_field_by_id_not_found(self, client: TestClient) -> None:
        """Test getting non-existent field."""
        response = client.get("/api/v1/fields/99999")
        
        assert response.status_code == 404
        data: dict[str, Any] = response.json()
        assert "detail" in data
        assert data["detail"] == "Field not found"

    def test_update_field_success(self, client: TestClient) -> None:
        """Test updating field."""
        # First create a field
        field_data: dict[str, str] = {"name": "Field to Update"}
        create_response = client.post("/api/v1/fields/", json=field_data)
        created_field: dict[str, Any] = create_response.json()["data"]
        
        # Update the field
        update_data: dict[str, str] = {"name": "Updated Field Name"}
        response = client.put(f"/api/v1/fields/{created_field['field_id']}", json=update_data)
        
        assert response.status_code == 200
        data: dict[str, Any] = response.json()
        assert data["success"] is True
        assert data["message"] == "Field updated successfully"
        assert data["data"]["name"] == "Updated Field Name"

    def test_update_field_not_found(self, client: TestClient) -> None:
        """Test updating non-existent field."""
        update_data: dict[str, str] = {"name": "Non-existent Field"}
        response = client.put("/api/v1/fields/99999", json=update_data)
        
        assert response.status_code == 404
        data: dict[str, Any] = response.json()
        assert "detail" in data
        assert data["detail"] == "Field not found"

    def test_delete_field_success(self, client: TestClient) -> None:
        """Test deleting field."""
        # First create a field
        field_data: dict[str, str] = {"name": "Field to Delete"}
        create_response = client.post("/api/v1/fields/", json=field_data)
        created_field: dict[str, Any] = create_response.json()["data"]
        
        # Delete the field
        response = client.delete(f"/api/v1/fields/{created_field['field_id']}")
        
        assert response.status_code == 204

    def test_delete_field_not_found(self, client: TestClient) -> None:
        """Test deleting non-existent field."""
        response = client.delete("/api/v1/fields/99999")
        
        assert response.status_code == 404
        data: dict[str, Any] = response.json()
        assert "detail" in data
        assert data["detail"] == "Field not found"
