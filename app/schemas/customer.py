"""
Customer API schemas for requests and responses.
"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime
from app.schemas.base import DataResponse, ListResponse

class CustomerBase(BaseModel):
    """Base customer model with common fields."""
    name: str = Field(..., min_length=1, max_length=255, description="Customer name")
    field_id: int = Field(..., description="Field ID")
    representative_name: str = Field(..., max_length=255, description="Representative name")
    representative_phone: str = Field(..., min_length=10, max_length=20, description="Representative phone")
    representative_email: EmailStr = Field(..., description="Representative email")
    representative_role: str = Field(..., max_length=100, description="Representative role")

class CustomerCreate(CustomerBase):
    """Schema for creating a new customer."""
    pass

class CustomerUpdate(BaseModel):
    """Schema for updating a customer."""
    name: Optional[str] = Field(None, min_length=1, max_length=255, description="Customer name")
    field_id: Optional[int] = Field(None, description="Field ID")
    representative_name: Optional[str] = Field(None, max_length=255, description="Representative name")
    representative_phone: Optional[str] = Field(None, min_length=10, max_length=20, description="Representative phone")
    representative_email: Optional[EmailStr] = Field(None, description="Representative email")
    representative_role: Optional[str] = Field(None, max_length=100, description="Representative role")

class CustomerResponse(CustomerBase):
    """Schema for customer response."""
    customer_id: int = Field(..., description="Unique customer ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        from_attributes = True

class CustomerDetailResponse(DataResponse[CustomerResponse]):
    """Response for single customer operations."""
    pass

class CustomerListResponse(ListResponse[CustomerResponse]):
    """Response for customer list operations."""
    pass
