"""
Unit tests for schema validation and utilities.
"""
import pytest
from datetime import datetime, date
from typing import Any
from pydantic import ValidationError
from app.schemas.area import AreaCreate, AreaUpdate, AreaResponse
from app.schemas.customer import CustomerCreate, CustomerUpdate
from app.schemas.project import ProjectCreate
from app.schemas.utils import create_list_response, entity_to_response_model
from app.core.entities.area import Area

class TestSchemaValidation:
    """Test schema validation rules."""
    
    def test_area_create_valid(self) -> None:
        """Test valid area creation schema."""
        area_data: AreaCreate = AreaCreate(name="Test Area")
        assert area_data.name == "Test Area"
    
    def test_area_create_empty_name(self) -> None:
        """Test area creation with empty name fails validation."""
        with pytest.raises(ValidationError):
            AreaCreate(name="")
    
    def test_area_create_long_name(self) -> None:
        """Test area creation with very long name."""
        long_name: str = "a" * 300  # Exceeds max length
        with pytest.raises(ValidationError):
            AreaCreate(name=long_name)
    
    def test_customer_create_valid(self) -> None:
        """Test valid customer creation schema."""
        customer_data: CustomerCreate = CustomerCreate(
            name="Test Customer",
            field_id=1,
            representative_name="John Doe",
            representative_phone="1234567890",
            representative_email="john@test.com",
            representative_role="Manager"
        )
        assert customer_data.name == "Test Customer"
        assert customer_data.representative_email == "john@test.com"
    
    def test_customer_create_invalid_email(self) -> None:
        """Test customer creation with invalid email fails validation."""
        with pytest.raises(ValidationError):
            CustomerCreate(
                name="Test Customer",
                field_id=1,
                representative_name="John Doe",
                representative_phone="1234567890",
                representative_email="invalid-email",
                representative_role="Manager"
            )
    
    def test_customer_create_invalid_phone(self) -> None:
        """Test customer creation with short phone fails validation."""
        with pytest.raises(ValidationError):
            CustomerCreate(
                name="Test Customer",
                field_id=1,
                representative_name="John Doe",
                representative_phone="123",  # Too short
                representative_email="test@test.com",
                representative_role="Manager"
            )
    
    def test_project_create_valid(self) -> None:
        """Test valid project creation schema."""
        project_data: ProjectCreate = ProjectCreate(
            name="Test Project",
            customer_id=1,
            description="Test description",
            status="ACTIVE",
            start_date=date(2024, 1, 1),
            end_date=date(2024, 12, 31),
            budget=100000.0
        )
        assert project_data.name == "Test Project"
        assert project_data.customer_id == 1
        assert project_data.budget == 100000.0
    
    def test_project_create_negative_budget(self) -> None:
        """Test project creation with negative budget fails validation."""
        with pytest.raises(ValidationError):
            ProjectCreate(
                name="Test Project",
                customer_id=1,
                description="Test description",
                status="ACTIVE",
                start_date=date(2024, 1, 1),
                end_date=date(2024, 12, 31),
                budget=-1000.0  # Negative budget
            )

class TestSchemaUtils:
    """Test schema utility functions."""
    
    def test_create_list_response(self) -> None:
        """Test creating list response with pagination."""
        now: datetime = datetime.now()
        data: list[AreaResponse] = [
            AreaResponse(area_id=1, name="Area 1", created_at=now, updated_at=now),
            AreaResponse(area_id=2, name="Area 2", created_at=now, updated_at=now),
        ]
        
        response = create_list_response(
            data=data,
            total=2,
            page=1,
            page_size=10,
            message="Areas retrieved successfully"
        )
        
        assert response.success is True
        assert response.message == "Areas retrieved successfully"
        assert len(response.data) == 2
        assert response.pagination.total == 2
        assert response.pagination.page == 1
        assert response.pagination.page_size == 10
    
    def test_entity_to_response_model(self) -> None:
        """Test converting entity to response model."""
        # Create a mock area entity
        now: datetime = datetime.now()
        area_entity: Area = Area(
            area_id=1,
            name="Test Area",
            created_at=now,
            updated_at=now
        )
        
        response_model: AreaResponse = entity_to_response_model(area_entity, AreaResponse)
        
        assert isinstance(response_model, AreaResponse)
        assert response_model.area_id == 1
        assert response_model.name == "Test Area"
        assert response_model.created_at is not None
        assert response_model.updated_at is not None

class TestSchemaUpdate:
    """Test update schema functionality."""
    
    def test_area_update_partial(self) -> None:
        """Test partial area update."""
        update_data: AreaUpdate = AreaUpdate(name="Updated Area")
        assert update_data.name == "Updated Area"
    
    def test_area_update_empty(self) -> None:
        """Test empty area update."""
        update_data: AreaUpdate = AreaUpdate()
        # Should not fail with no fields provided
        excluded_data: dict[str, Any] = update_data.model_dump(exclude_unset=True)
        assert excluded_data == {}
    
    def test_customer_update_email_only(self) -> None:
        """Test updating only customer email."""
        update_data: CustomerUpdate = CustomerUpdate(
            representative_email="newemail@test.com"
        )
        dumped: dict[str, Any] = update_data.model_dump(exclude_unset=True)
        assert "representative_email" in dumped
        assert "name" not in dumped
        assert dumped["representative_email"] == "newemail@test.com"
