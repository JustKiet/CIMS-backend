"""
Test cases for Nominee API endpoints
"""
from typing import Any

import pytest # type: ignore
from fastapi.testclient import TestClient


class TestNomineeAPI:
    """Test suite for Nominee API endpoints."""

    @staticmethod
    def get_valid_nominee_data() -> dict[str, Any]:
        """Helper method to get valid nominee data."""
        return {
            "candidate_id": 1,
            "project_id": 1,
            "status": "DECU",
            "campaign": "Q1 2024 Campaign",
            "years_of_experience": 5,
            "salary_expectation": 75000.0,
            "notice_period": 30
        }

    def test_create_nominee_success(self, client: TestClient) -> None:
        """Test creating new nominee successfully."""
        nominee_data = self.get_valid_nominee_data()

        response = client.post("/api/v1/nominees/", json=nominee_data)

        assert response.status_code == 201
        data: dict[str, Any] = response.json()
        assert data["success"] is True
        assert data["message"] == "Nominee created successfully"
        assert "data" in data
        assert data["data"]["candidate_id"] == 1
        assert data["data"]["project_id"] == 1
        assert data["data"]["status"] == "DECU"
        assert "nominee_id" in data["data"]

    def test_create_nominee_invalid_data(self, client: TestClient) -> None:
        """Test creating nominee with invalid data."""
        invalid_data: dict[str, str] = {"invalid_field": "test"}
        
        response = client.post("/api/v1/nominees/", json=invalid_data)
        
        assert response.status_code == 422

    def test_create_nominee_invalid_status(self, client: TestClient) -> None:
        """Test creating nominee with invalid status."""
        nominee_data = self.get_valid_nominee_data()
        nominee_data["status"] = "INVALID_STATUS"

        response = client.post("/api/v1/nominees/", json=nominee_data)
        
        assert response.status_code == 422

    def test_create_nominee_invalid_ids(self, client: TestClient) -> None:
        """Test creating nominee with invalid IDs."""
        nominee_data = self.get_valid_nominee_data()
        nominee_data["candidate_id"] = -1
        nominee_data["project_id"] = -1

        response = client.post("/api/v1/nominees/", json=nominee_data)
        
        assert response.status_code == 422

    def test_get_nominees_pagination(self, client: TestClient) -> None:
        """Test getting nominees with pagination."""
        # First create some nominees
        for i in range(3):
            nominee_data = self.get_valid_nominee_data()
            nominee_data["campaign"] = f"Campaign {i + 1}"
            client.post("/api/v1/nominees/", json=nominee_data)

        response = client.get("/api/v1/nominees/?page=1&page_size=2")

        assert response.status_code == 200
        data: dict[str, Any] = response.json()
        assert data["success"] is True
        assert "data" in data
        assert len(data["data"]) <= 2

    def test_search_nominees(self, client: TestClient) -> None:
        """Test searching nominees by status."""
        # Create a nominee to search for
        nominee_data = self.get_valid_nominee_data()
        nominee_data["status"] = "PHONGVAN"
        nominee_data["campaign"] = "Interview Campaign"
        client.post("/api/v1/nominees/", json=nominee_data)

        response = client.get("/api/v1/nominees/search?query=PHONGVAN")

        assert response.status_code == 200
        data: dict[str, Any] = response.json()
        assert data["success"] is True

    def test_get_nominee_by_id_success(self, client: TestClient) -> None:
        """Test getting nominee by ID."""
        # First create a nominee
        nominee_data = self.get_valid_nominee_data()
        nominee_data["status"] = "THUONGLUONG"
        nominee_data["campaign"] = "Negotiation Campaign"
        create_response = client.post("/api/v1/nominees/", json=nominee_data)
        created_nominee: dict[str, Any] = create_response.json()["data"]

        response = client.get(f"/api/v1/nominees/{created_nominee['nominee_id']}")

        assert response.status_code == 200
        data: dict[str, Any] = response.json()
        assert data["success"] is True
        assert data["data"]["nominee_id"] == created_nominee["nominee_id"]

    def test_get_nominee_by_id_not_found(self, client: TestClient) -> None:
        """Test getting non-existent nominee."""
        response = client.get("/api/v1/nominees/99999")

        assert response.status_code == 404

    def test_update_nominee_success(self, client: TestClient) -> None:
        """Test updating nominee."""
        # First create a nominee
        nominee_data = self.get_valid_nominee_data()
        nominee_data["campaign"] = "Initial Campaign"
        create_response = client.post("/api/v1/nominees/", json=nominee_data)
        created_nominee: dict[str, Any] = create_response.json()["data"]

        # Update the nominee
        update_data: dict[str, Any] = {
            "status": "PHONGVAN",
            "campaign": "Updated Campaign"
        }
        response = client.put(f"/api/v1/nominees/{created_nominee['nominee_id']}", json=update_data)

        assert response.status_code == 200
        data: dict[str, Any] = response.json()
        assert data["success"] is True
        assert data["data"]["status"] == "PHONGVAN"
        assert data["data"]["campaign"] == "Updated Campaign"

    def test_update_nominee_not_found(self, client: TestClient) -> None:
        """Test updating non-existent nominee."""
        update_data: dict[str, str] = {"status": "PHONGVAN"}

        response = client.put("/api/v1/nominees/99999", json=update_data)

        assert response.status_code == 404

    def test_delete_nominee_success(self, client: TestClient) -> None:
        """Test deleting nominee."""
        # First create a nominee
        nominee_data = self.get_valid_nominee_data()
        nominee_data["status"] = "TUCHOI"
        nominee_data["campaign"] = "To be deleted"
        create_response = client.post("/api/v1/nominees/", json=nominee_data)
        created_nominee: dict[str, Any] = create_response.json()["data"]

        # Delete the nominee
        response = client.delete(f"/api/v1/nominees/{created_nominee['nominee_id']}")

        assert response.status_code == 204

        # Verify it's deleted
        get_response = client.get(f"/api/v1/nominees/{created_nominee['nominee_id']}")
        assert get_response.status_code == 404

    def test_delete_nominee_not_found(self, client: TestClient) -> None:
        """Test deleting non-existent nominee."""
        response = client.delete("/api/v1/nominees/99999")

        assert response.status_code == 404

    def test_nominee_status_transitions(self, client: TestClient) -> None:
        """Test various nominee status values."""
        statuses = ["DECU", "PHONGVAN", "THUONGLUONG", "THUVIEC", "TUCHOI", "KYHOPDONG"]

        for status in statuses:
            nominee_data = self.get_valid_nominee_data()
            nominee_data["status"] = status
            nominee_data["campaign"] = f"Testing {status} status"

            response = client.post("/api/v1/nominees/", json=nominee_data)

            assert response.status_code == 201
            data: dict[str, Any] = response.json()
            assert data["data"]["status"] == status
