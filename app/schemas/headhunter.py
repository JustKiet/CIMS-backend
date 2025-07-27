"""
Headhunter API schemas for requests and responses.
"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime
from app.schemas.base import DataResponse, ListResponse

class HeadhunterBase(BaseModel):
    """Base headhunter model with common fields."""
    name: str = Field(..., min_length=1, max_length=255, description="Headhunter full name")
    phone: str = Field(..., min_length=10, max_length=20, description="Phone number")
    email: EmailStr = Field(..., description="Email address")
    area_id: int = Field(..., gt=0, description="Area ID")
    role: str = Field(default="headhunter", max_length=50, description="Role in the system")

class HeadhunterCreate(HeadhunterBase):
    """Schema for creating a new headhunter."""
    password: str = Field(..., min_length=8, max_length=255, description="Password (will be hashed)")

class HeadhunterUpdate(BaseModel):
    """Schema for updating a headhunter."""
    name: Optional[str] = Field(None, min_length=1, max_length=255, description="Headhunter full name")
    phone: Optional[str] = Field(None, min_length=10, max_length=20, description="Phone number")
    email: Optional[EmailStr] = Field(None, description="Email address")
    area_id: Optional[int] = Field(None, gt=0, description="Area ID")
    role: Optional[str] = Field(None, max_length=50, description="Role in the system")

class HeadhunterPasswordUpdate(BaseModel):
    """Schema for updating headhunter password."""
    current_password: str = Field(..., description="Current password")
    new_password: str = Field(..., min_length=8, max_length=255, description="New password")

class HeadhunterResponse(HeadhunterBase):
    """Schema for headhunter response."""
    headhunter_id: int = Field(..., description="Unique headhunter ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        from_attributes = True

class HeadhunterDetailResponse(DataResponse[HeadhunterResponse]):
    """Response for single headhunter operations."""
    pass

class HeadhunterListResponse(ListResponse[HeadhunterResponse]):
    """Response for headhunter list operations."""
    pass
