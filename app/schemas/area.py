"""
Area API schemas for requests and responses.
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.schemas.base import DataResponse, ListResponse

class AreaBase(BaseModel):
    """Base area model with common fields."""
    name: str = Field(..., min_length=1, max_length=255, description="Area name")

class AreaCreate(AreaBase):
    """Schema for creating a new area."""
    pass

class AreaUpdate(BaseModel):
    """Schema for updating an area."""
    name: Optional[str] = Field(None, min_length=1, max_length=255, description="Area name")

class AreaResponse(AreaBase):
    """Schema for area response."""
    area_id: int = Field(..., description="Unique area ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        from_attributes = True

class AreaDetailResponse(DataResponse[AreaResponse]):
    """Response for single area operations."""
    pass

class AreaListResponse(ListResponse[AreaResponse]):
    """Response for area list operations."""
    pass
