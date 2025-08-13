"""
Test cases for Candidate API endpoints
"""
from typing import Any

from fastapi.testclient import TestClient


class TestCandidateAPI:
    """Test class for candidate-related endpoints."""

    def test_create_candidate_success(self, client: TestClient) -> None:
        """Test creating new candidate successfully."""
        candidate_data: dict[str, Any] = {
            "name": "John Smith",
            "phone": "1234567890",
            "email": "john.smith@email.com",
            "year_of_birth": 1990,
            "gender": "NAM",
            "education": "Bachelor of Computer Science",
            "source": "LinkedIn",
            "expertise_id": 1,
            "field_id": 1,
            "area_id": 1,
            "level_id": 1,
            "headhunter_id": 1,
            "note": "Experienced developer"
        }
        
        response = client.post("/api/v1/candidates/", json=candidate_data)
        
        assert response.status_code == 201
        data: dict[str, Any] = response.json()
        assert data["success"] is True
        assert data["message"] == "Candidate created successfully"
        assert "data" in data
        assert data["data"]["name"] == "John Smith"
        assert data["data"]["email"] == "john.smith@email.com"
        assert data["data"]["gender"] == "NAM"
        assert "candidate_id" in data["data"]

    def test_create_candidate_invalid_data(self, client: TestClient) -> None:
        """Test creating candidate with invalid data."""
        invalid_data: dict[str, str] = {"invalid_field": "test"}
        
        response = client.post("/api/v1/candidates/", json=invalid_data)
        
        assert response.status_code == 422

    def test_create_candidate_invalid_gender(self, client: TestClient) -> None:
        """Test creating candidate with invalid gender."""
        candidate_data: dict[str, Any] = {
            "name": "Test User",
            "phone": "1234567890",
            "email": "test@email.com",
            "year_of_birth": 1990,
            "gender": "INVALID",
            "education": "Bachelor",
            "source": "Test",
            "expertise_id": 1,
            "field_id": 1,
            "area_id": 1,
            "level_id": 1,
            "headhunter_id": 1
        }
        
        response = client.post("/api/v1/candidates/", json=candidate_data)
        
        assert response.status_code == 422

    def test_create_candidate_invalid_year(self, client: TestClient) -> None:
        """Test creating candidate with invalid year of birth."""
        candidate_data: dict[str, Any] = {
            "name": "Test User",
            "phone": "1234567890",
            "email": "test@email.com",
            "year_of_birth": 1800,  # Too old
            "gender": "NAM",
            "education": "Bachelor",
            "source": "Test",
            "expertise_id": 1,
            "field_id": 1,
            "area_id": 1,
            "level_id": 1,
            "headhunter_id": 1
        }
        
        response = client.post("/api/v1/candidates/", json=candidate_data)
        
        assert response.status_code == 422

    def test_get_candidates_pagination(self, client: TestClient) -> None:
        """Test getting candidates with pagination."""
        # First create some candidates
        for i in range(3):
            candidate_data: dict[str, Any] = {
                "name": f"Test Candidate {i}",
                "phone": f"123456789{i}",
                "email": f"test{i}@email.com",
                "year_of_birth": 1990 + i,
                "gender": "NAM",
                "education": "Bachelor",
                "source": "Test",
                "expertise_id": 1,
                "field_id": 1,
                "area_id": 1,
                "level_id": 1,
                "headhunter_id": 1
            }
            client.post("/api/v1/candidates/", json=candidate_data)
        
        response = client.get("/api/v1/candidates/?page=1&page_size=2")
        
        assert response.status_code == 200
        data: dict[str, Any] = response.json()
        assert data["success"] is True
        assert "data" in data
        assert len(data["data"]) <= 2
        assert "pagination" in data

    def test_search_candidates(self, client: TestClient) -> None:
        """Test searching candidates by name."""
        # Create a candidate to search for
        candidate_data: dict[str, Any] = {
            "name": "Searchable Candidate",
            "phone": "1234567890",
            "email": "searchable@email.com",
            "year_of_birth": 1990,
            "gender": "NU",
            "education": "Master's Degree",
            "source": "Job Fair",
            "expertise_id": 1,
            "field_id": 1,
            "area_id": 1,
            "level_id": 1,
            "headhunter_id": 1
        }
        client.post("/api/v1/candidates/", json=candidate_data)
        
        response = client.get("/api/v1/candidates/search?query=Searchable")
        
        assert response.status_code == 200
        data: dict[str, Any] = response.json()
        assert data["success"] is True
        assert "data" in data

    def test_get_candidate_by_id_success(self, client: TestClient) -> None:
        """Test getting candidate by ID."""
        # First create a candidate
        candidate_data: dict[str, Any] = {
            "name": "Get Test Candidate",
            "phone": "1234567890",
            "email": "gettest@email.com",
            "year_of_birth": 1995,
            "gender": "KHAC",
            "education": "PhD",
            "source": "Referral",
            "expertise_id": 1,
            "field_id": 1,
            "area_id": 1,
            "level_id": 1,
            "headhunter_id": 1
        }
        create_response = client.post("/api/v1/candidates/", json=candidate_data)
        created_candidate: dict[str, Any] = create_response.json()["data"]
        
        response = client.get(f"/api/v1/candidates/{created_candidate['candidate_id']}")
        
        assert response.status_code == 200
        data: dict[str, Any] = response.json()
        assert data["success"] is True
        assert data["data"]["name"] == "Get Test Candidate"
        assert data["data"]["candidate_id"] == created_candidate["candidate_id"]

    def test_get_candidate_by_id_not_found(self, client: TestClient) -> None:
        """Test getting non-existent candidate."""
        response = client.get("/api/v1/candidates/99999")
        
        assert response.status_code == 404
        data: dict[str, Any] = response.json()
        assert "detail" in data
        assert data["detail"] == "Candidate not found"

    def test_update_candidate_success(self, client: TestClient) -> None:
        """Test updating candidate."""
        # First create a candidate
        candidate_data: dict[str, Any] = {
            "name": "Candidate to Update",
            "phone": "1234567890",
            "email": "update@email.com",
            "year_of_birth": 1990,
            "gender": "NAM",
            "education": "Bachelor",
            "source": "Test",
            "expertise_id": 1,
            "field_id": 1,
            "area_id": 1,
            "level_id": 1,
            "headhunter_id": 1
        }
        create_response = client.post("/api/v1/candidates/", json=candidate_data)
        created_candidate: dict[str, Any] = create_response.json()["data"]
        
        # Update the candidate
        update_data: dict[str, str] = {"name": "Updated Candidate Name"}
        response = client.put(f"/api/v1/candidates/{created_candidate['candidate_id']}", json=update_data)
        
        assert response.status_code == 200
        data: dict[str, Any] = response.json()
        assert data["success"] is True
        assert data["message"] == "Candidate updated successfully"
        assert data["data"]["name"] == "Updated Candidate Name"

    def test_update_candidate_not_found(self, client: TestClient) -> None:
        """Test updating non-existent candidate."""
        update_data: dict[str, str] = {"name": "Non-existent Candidate"}
        response = client.put("/api/v1/candidates/99999", json=update_data)
        
        assert response.status_code == 404
        data: dict[str, Any] = response.json()
        assert "detail" in data
        assert data["detail"] == "Candidate not found"

    def test_delete_candidate_success(self, client: TestClient) -> None:
        """Test deleting candidate."""
        # First create a candidate
        candidate_data: dict[str, Any] = {
            "name": "Candidate to Delete",
            "phone": "1234567890",
            "email": "delete@email.com",
            "year_of_birth": 1990,
            "gender": "NAM",
            "education": "Bachelor",
            "source": "Test",
            "expertise_id": 1,
            "field_id": 1,
            "area_id": 1,
            "level_id": 1,
            "headhunter_id": 1
        }
        create_response = client.post("/api/v1/candidates/", json=candidate_data)
        created_candidate: dict[str, Any] = create_response.json()["data"]
        
        # Delete the candidate
        response = client.delete(f"/api/v1/candidates/{created_candidate['candidate_id']}")
        
        assert response.status_code == 204

    def test_delete_candidate_not_found(self, client: TestClient) -> None:
        """Test deleting non-existent candidate."""
        response = client.delete("/api/v1/candidates/99999")
        
        assert response.status_code == 404
        data: dict[str, Any] = response.json()
        assert "detail" in data
        assert data["detail"] == "Candidate not found"
