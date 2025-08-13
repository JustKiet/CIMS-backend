"""
Test cases for Expertise API endpoints
"""
from typing import Any

from fastapi.testclient import TestClient


class TestExpertiseAPI:
    """Test class for expertise-related endpoints."""

    def test_create_expertise_success(self, client: TestClient) -> None:
        """Test creating new expertise successfully."""
        expertise_data: dict[str, str] = {"name": "Python Development"}
        
        response = client.post("/api/v1/expertises/", json=expertise_data)
        
        assert response.status_code == 201
        data: dict[str, Any] = response.json()
        assert data["success"] is True
        assert data["message"] == "Expertise created successfully"
        assert "data" in data
        assert data["data"]["name"] == "Python Development"
        assert "expertise_id" in data["data"]

    def test_create_expertise_invalid_data(self, client: TestClient) -> None:
        """Test creating expertise with invalid data."""
        invalid_data: dict[str, str] = {"invalid_field": "test"}
        
        response = client.post("/api/v1/expertises/", json=invalid_data)
        
        assert response.status_code == 422

    def test_get_expertises_pagination(self, client: TestClient) -> None:
        """Test getting expertises with pagination."""
        # First create some expertises
        for i in range(3):
            expertise_data: dict[str, str] = {"name": f"Test Expertise {i}"}
            client.post("/api/v1/expertises/", json=expertise_data)
        
        response = client.get("/api/v1/expertises/?page=1&page_size=2")
        
        assert response.status_code == 200
        data: dict[str, Any] = response.json()
        assert data["success"] is True
        assert "data" in data
        assert len(data["data"]) <= 2
        assert "pagination" in data

    def test_search_expertises(self, client: TestClient) -> None:
        """Test searching expertises by name."""
        # Create an expertise to search for
        expertise_data: dict[str, str] = {"name": "Data Science"}
        client.post("/api/v1/expertises/", json=expertise_data)
        
        response = client.get("/api/v1/expertises/search?query=Data")
        
        assert response.status_code == 200
        data: dict[str, Any] = response.json()
        assert data["success"] is True
        assert "data" in data

    def test_get_expertise_by_id_success(self, client: TestClient) -> None:
        """Test getting expertise by ID."""
        # First create an expertise
        expertise_data: dict[str, str] = {"name": "Machine Learning"}
        create_response = client.post("/api/v1/expertises/", json=expertise_data)
        created_expertise: dict[str, Any] = create_response.json()["data"]
        
        response = client.get(f"/api/v1/expertises/{created_expertise['expertise_id']}")
        
        assert response.status_code == 200
        data: dict[str, Any] = response.json()
        assert data["success"] is True
        assert data["data"]["name"] == "Machine Learning"
        assert data["data"]["expertise_id"] == created_expertise["expertise_id"]

    def test_get_expertise_by_id_not_found(self, client: TestClient) -> None:
        """Test getting non-existent expertise."""
        response = client.get("/api/v1/expertises/99999")
        
        assert response.status_code == 404
        data: dict[str, Any] = response.json()
        assert "detail" in data
        assert data["detail"] == "Expertise not found"

    def test_update_expertise_success(self, client: TestClient) -> None:
        """Test updating expertise."""
        # First create an expertise
        expertise_data: dict[str, str] = {"name": "Expertise to Update"}
        create_response = client.post("/api/v1/expertises/", json=expertise_data)
        created_expertise: dict[str, Any] = create_response.json()["data"]
        
        # Update the expertise
        update_data: dict[str, str] = {"name": "Updated Expertise Name"}
        response = client.put(f"/api/v1/expertises/{created_expertise['expertise_id']}", json=update_data)
        
        assert response.status_code == 200
        data: dict[str, Any] = response.json()
        assert data["success"] is True
        assert data["message"] == "Expertise updated successfully"
        assert data["data"]["name"] == "Updated Expertise Name"

    def test_update_expertise_not_found(self, client: TestClient) -> None:
        """Test updating non-existent expertise."""
        update_data: dict[str, str] = {"name": "Non-existent Expertise"}
        response = client.put("/api/v1/expertises/99999", json=update_data)
        
        assert response.status_code == 404
        data: dict[str, Any] = response.json()
        assert "detail" in data
        assert data["detail"] == "Expertise not found"

    def test_delete_expertise_success(self, client: TestClient) -> None:
        """Test deleting expertise."""
        # First create an expertise
        expertise_data: dict[str, str] = {"name": "Expertise to Delete"}
        create_response = client.post("/api/v1/expertises/", json=expertise_data)
        created_expertise: dict[str, Any] = create_response.json()["data"]
        
        # Delete the expertise
        response = client.delete(f"/api/v1/expertises/{created_expertise['expertise_id']}")
        
        assert response.status_code == 204

    def test_delete_expertise_not_found(self, client: TestClient) -> None:
        """Test deleting non-existent expertise."""
        response = client.delete("/api/v1/expertises/99999")
        
        assert response.status_code == 404
        data: dict[str, Any] = response.json()
        assert "detail" in data
        assert data["detail"] == "Expertise not found"
