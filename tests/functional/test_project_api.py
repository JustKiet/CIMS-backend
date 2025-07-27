"""
Functional tests for Project API endpoints.
Tests all CRUD operations with complex project data.
"""
import pytest # type: ignore
from typing import Any
from fastapi.testclient import TestClient
from datetime import date # type: ignore

class TestProjectAPI:
    """Test suite for Project API endpoints."""
    
    def test_create_project_success(self, client: TestClient) -> None:
        """Test successful project creation."""
        project_data: dict[str, Any] = {
            "name": "Test Project",
            "customer_id": 1,
            "description": "A test project for API validation",
            "status": "ACTIVE",
            "start_date": "2024-01-01",
            "end_date": "2024-12-31",
            "budget": 100000.0
        }
        
        response = client.post("/api/v1/projects/", json=project_data)
        
        assert response.status_code == 201
        data: dict[str, Any] = response.json()  # type: ignore
        assert data["success"] is True
        assert data["message"] == "Project created successfully"
        assert "data" in data
        assert data["data"]["name"] == "Test Project"
        assert "project_id" in data["data"]

    def test_create_project_invalid_data(self, client: TestClient) -> None:
        """Test project creation with invalid data."""
        invalid_data: dict[str, str] = {"invalid_field": "test"}
        
        response = client.post("/api/v1/projects/", json=invalid_data)
        
        assert response.status_code == 422

    def test_get_projects_pagination(self, client: TestClient) -> None:
        """Test getting projects with pagination."""
        # First create some projects
        for i in range(3):
            project_data: dict[str, Any] = {
                "name": f"Test Project {i}",
                "customer_id": 1,
                "description": f"Test project {i}",
                "status": "ACTIVE",
                "start_date": "2024-01-01",
                "end_date": "2024-12-31",
                "budget": 50000.0 + i * 10000
            }
            client.post("/api/v1/projects/", json=project_data)
        
        response = client.get("/api/v1/projects/?page=1&page_size=2")
        
        assert response.status_code == 200
        data: dict[str, Any] = response.json()
        assert data["success"] is True
        assert "data" in data
        assert len(data["data"]) <= 2

    def test_search_projects(self, client: TestClient) -> None:
        """Test searching projects by name."""
        # Create a project to search for
        project_data: dict[str, Any] = {
            "name": "Searchable Project",
            "customer_id": 1,
            "description": "A searchable project",
            "status": "ACTIVE",
            "start_date": "2024-01-01",
            "end_date": "2024-12-31",
            "budget": 75000.0
        }
        client.post("/api/v1/projects/", json=project_data)
        
        response = client.get("/api/v1/projects/search?query=Searchable")
        
        assert response.status_code == 200
        data: dict[str, Any] = response.json()
        assert data["success"] is True
        assert "data" in data

    def test_get_project_by_id_success(self, client: TestClient) -> None:
        """Test getting project by ID."""
        # First create a project
        project_data: dict[str, Any] = {
            "name": "Get Project Test",
            "customer_id": 1,
            "description": "Test getting project",
            "status": "ACTIVE",
            "start_date": "2024-01-01",
            "end_date": "2024-12-31",
            "budget": 80000.0
        }
        create_response = client.post("/api/v1/projects/", json=project_data)
        created_project: dict[str, Any] = create_response.json()["data"]
        
        response = client.get(f"/api/v1/projects/{created_project['project_id']}")
        
        assert response.status_code == 200
        data: dict[str, Any] = response.json()
        assert data["success"] is True
        assert data["data"]["name"] == "Get Project Test"
        assert data["data"]["project_id"] == created_project["project_id"]

    def test_get_project_by_id_not_found(self, client: TestClient) -> None:
        """Test getting non-existent project."""
        response = client.get("/api/v1/projects/99999")
        
        assert response.status_code == 404
        data: dict[str, Any] = response.json()
        assert "detail" in data
        assert data["detail"] == "Project not found"

    def test_update_project_success(self, client: TestClient) -> None:
        """Test updating project."""
        # First create a project
        project_data: dict[str, Any] = {
            "name": "Update Project Test",
            "customer_id": 1,
            "description": "Test updating project",
            "status": "ACTIVE",
            "start_date": "2024-01-01",
            "end_date": "2024-12-31",
            "budget": 90000.0
        }
        create_response = client.post("/api/v1/projects/", json=project_data)
        created_project: dict[str, Any] = create_response.json()["data"]
        
        # Update the project
        update_data: dict[str, str] = {"name": "Updated Project Name"}
        response = client.put(f"/api/v1/projects/{created_project['project_id']}", json=update_data)
        
        assert response.status_code == 200
        data: dict[str, Any] = response.json()
        assert data["success"] is True
        assert data["message"] == "Project updated successfully"
        assert data["data"]["name"] == "Updated Project Name"

    def test_update_project_not_found(self, client: TestClient) -> None:
        """Test updating non-existent project."""
        update_data: dict[str, str] = {"name": "Non-existent Project"}
        response = client.put("/api/v1/projects/99999", json=update_data)
        
        assert response.status_code == 404
        data: dict[str, Any] = response.json()
        assert "detail" in data
        assert data["detail"] == "Project not found"

    def test_delete_project_success(self, client: TestClient) -> None:
        """Test deleting project."""
        # First create a project
        project_data: dict[str, Any] = {
            "name": "Delete Project Test",
            "customer_id": 1,
            "description": "Test deleting project",
            "status": "ACTIVE",
            "start_date": "2024-01-01",
            "end_date": "2024-12-31",
            "budget": 85000.0
        }
        create_response = client.post("/api/v1/projects/", json=project_data)
        created_project: dict[str, Any] = create_response.json()["data"]
        
        # Delete the project
        response = client.delete(f"/api/v1/projects/{created_project['project_id']}")
        
        assert response.status_code == 204

    def test_delete_project_not_found(self, client: TestClient) -> None:
        """Test deleting non-existent project."""
        response = client.delete("/api/v1/projects/99999")
        
        assert response.status_code == 404
        data: dict[str, Any] = response.json()
        assert "detail" in data
        assert data["detail"] == "Project not found"
