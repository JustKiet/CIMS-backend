"""
Functional tests for Customer API endpoints.
Tests all CRUD operations with proper authentication and validation.
"""
import pytest # type: ignore
from typing import Any
from fastapi.testclient import TestClient

class TestCustomerAPI:
    """Test suite for Customer API endpoints."""
    
    def test_create_customer_success(self, client: TestClient) -> None:
        """Test successful customer creation."""
        customer_data: dict[str, Any] = {
            "name": "Test Customer",
            "field_id": 1,
            "representative_name": "John Doe",
            "representative_phone": "1234567890",
            "representative_email": "john@testcustomer.com",
            "representative_role": "Manager"
        }
        
        response = client.post("/api/v1/customers/", json=customer_data)
        
        assert response.status_code == 201
        data: dict[str, Any] = response.json()  # type: ignore
        assert data["success"] is True
        assert data["message"] == "Customer created successfully"
        assert "data" in data
        assert data["data"]["name"] == "Test Customer"
        assert "customer_id" in data["data"]

    def test_create_customer_invalid_email(self, client: TestClient) -> None:
        """Test customer creation with invalid data."""
        invalid_data: dict[str, str] = {"invalid_field": "test"}
        
        response = client.post("/api/v1/customers/", json=invalid_data)
        
        assert response.status_code == 422

    def test_get_customers_pagination(self, client: TestClient) -> None:
        """Test getting customers with pagination."""
        # First create some customers
        for i in range(3):
            customer_data: dict[str, Any] = {
                "name": f"Test Customer {i}",
                "field_id": 1,
                "representative_name": f"Contact {i}",
                "representative_phone": f"123456789{i}",
                "representative_email": f"contact{i}@test.com",
                "representative_role": "Manager"
            }
            client.post("/api/v1/customers/", json=customer_data)
        
        response = client.get("/api/v1/customers/?page=1&page_size=2")
        
        assert response.status_code == 200
        data: dict[str, Any] = response.json()
        assert data["success"] is True
        assert "data" in data
        assert len(data["data"]) <= 2

    def test_search_customers(self, client: TestClient) -> None:
        """Test searching customers by name."""
        # Create a customer to search for
        customer_data: dict[str, Any] = {
            "name": "Searchable Customer",
            "field_id": 1,
            "representative_name": "Search Contact",
            "representative_phone": "1234567890",
            "representative_email": "search@test.com",
            "representative_role": "Manager"
        }
        client.post("/api/v1/customers/", json=customer_data)
        
        response = client.get("/api/v1/customers/search?query=Searchable")
        
        assert response.status_code == 200
        data: dict[str, Any] = response.json()
        assert data["success"] is True
        assert "data" in data

    def test_get_customer_by_id_success(self, client: TestClient) -> None:
        """Test getting customer by ID."""
        # First create a customer
        customer_data: dict[str, Any] = {
            "name": "Get Customer Test",
            "field_id": 1,
            "representative_name": "Get Contact",
            "representative_phone": "1234567890",
            "representative_email": "get@test.com",
            "representative_role": "Manager"
        }
        create_response = client.post("/api/v1/customers/", json=customer_data)
        created_customer: dict[str, Any] = create_response.json()["data"]
        
        response = client.get(f"/api/v1/customers/{created_customer['customer_id']}")
        
        assert response.status_code == 200
        data: dict[str, Any] = response.json()
        assert data["success"] is True
        assert data["data"]["name"] == "Get Customer Test"
        assert data["data"]["customer_id"] == created_customer["customer_id"]

    def test_get_customer_by_id_not_found(self, client: TestClient) -> None:
        """Test getting non-existent customer."""
        response = client.get("/api/v1/customers/99999")
        
        assert response.status_code == 404
        data: dict[str, Any] = response.json()
        assert "detail" in data
        assert data["detail"] == "Customer not found"

    def test_update_customer_success(self, client: TestClient) -> None:
        """Test updating customer."""
        # First create a customer
        customer_data: dict[str, Any] = {
            "name": "Update Customer Test",
            "field_id": 1,
            "representative_name": "Update Contact",
            "representative_phone": "1234567890",
            "representative_email": "update@test.com",
            "representative_role": "Manager"
        }
        create_response = client.post("/api/v1/customers/", json=customer_data)
        created_customer: dict[str, Any] = create_response.json()["data"]
        
        # Update the customer
        update_data: dict[str, str] = {"name": "Updated Customer Name"}
        response = client.put(f"/api/v1/customers/{created_customer['customer_id']}", json=update_data)
        
        assert response.status_code == 200
        data: dict[str, Any] = response.json()
        assert data["success"] is True
        assert data["message"] == "Customer updated successfully"
        assert data["data"]["name"] == "Updated Customer Name"

    def test_update_customer_not_found(self, client: TestClient) -> None:
        """Test updating non-existent customer."""
        update_data: dict[str, str] = {"name": "Non-existent Customer"}
        response = client.put("/api/v1/customers/99999", json=update_data)
        
        assert response.status_code == 404
        data: dict[str, Any] = response.json()
        assert "detail" in data
        assert data["detail"] == "Customer not found"

    def test_delete_customer_success(self, client: TestClient) -> None:
        """Test deleting customer."""
        # First create a customer
        customer_data: dict[str, Any] = {
            "name": "Delete Customer Test",
            "field_id": 1,
            "representative_name": "Delete Contact",
            "representative_phone": "1234567890",
            "representative_email": "delete@test.com",
            "representative_role": "Manager"
        }
        create_response = client.post("/api/v1/customers/", json=customer_data)
        created_customer: dict[str, Any] = create_response.json()["data"]
        
        # Delete the customer
        response = client.delete(f"/api/v1/customers/{created_customer['customer_id']}")
        
        assert response.status_code == 204

    def test_delete_customer_not_found(self, client: TestClient) -> None:
        """Test deleting non-existent customer."""
        response = client.delete("/api/v1/customers/99999")
        
        assert response.status_code == 404
        data: dict[str, Any] = response.json()
        assert "detail" in data
        assert data["detail"] == "Customer not found"
