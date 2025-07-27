"""
Expertise API schemas for requests and responses.
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.schemas.base import DataResponse, ListResponse

class ExpertiseBase(BaseModel):
    """Base expertise model with common fields."""
    name: str = Field(..., min_length=1, max_length=255, description="Expertise name")

class ExpertiseCreate(ExpertiseBase):
    """Schema for creating a new expertise."""
    pass

class ExpertiseUpdate(BaseModel):
    """Schema for updating an expertise."""
    name: Optional[str] = Field(None, min_length=1, max_length=255, description="Expertise name")

class ExpertiseResponse(ExpertiseBase):
    """Schema for expertise response."""
    expertise_id: int = Field(..., description="Unique expertise ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        from_attributes = True

class ExpertiseDetailResponse(DataResponse[ExpertiseResponse]):
    """Response for single expertise operations."""
    pass

class ExpertiseListResponse(ListResponse[ExpertiseResponse]):
    """Response for expertise list operations."""
    pass
