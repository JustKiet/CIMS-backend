"""
Level API schemas for requests and responses.
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.schemas.base import DataResponse, ListResponse

class LevelBase(BaseModel):
    """Base level model with common fields."""
    name: str = Field(..., min_length=1, max_length=255, description="Level name")

class LevelCreate(LevelBase):
    """Schema for creating a new level."""
    pass

class LevelUpdate(BaseModel):
    """Schema for updating a level."""
    name: Optional[str] = Field(None, min_length=1, max_length=255, description="Level name")

class LevelResponse(LevelBase):
    """Schema for level response."""
    level_id: int = Field(..., description="Unique level ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        from_attributes = True

class LevelDetailResponse(DataResponse[LevelResponse]):
    """Response for single level operations."""
    pass

class LevelListResponse(ListResponse[LevelResponse]):
    """Response for level list operations."""
    pass
