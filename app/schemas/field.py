"""
Field API schemas for requests and responses.
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.schemas.base import DataResponse, ListResponse

class FieldBase(BaseModel):
    """Base field model with common fields."""
    name: str = Field(..., min_length=1, max_length=255, description="Field name")

class FieldCreate(FieldBase):
    """Schema for creating a new field."""
    pass

class FieldUpdate(BaseModel):
    """Schema for updating a field."""
    name: Optional[str] = Field(None, min_length=1, max_length=255, description="Field name")

class FieldResponse(FieldBase):
    """Schema for field response."""
    field_id: int = Field(..., description="Unique field ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        from_attributes = True

class FieldDetailResponse(DataResponse[FieldResponse]):
    """Response for single field operations."""
    pass

class FieldListResponse(ListResponse[FieldResponse]):
    """Response for field list operations."""
    pass
