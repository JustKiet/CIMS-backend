"""
Candidate API schemas for requests and responses.
"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime
from cims.core.entities.candidate import Gender
from cims.schemas.base import DataResponse, ListResponse

class CandidateBase(BaseModel):
    """Base candidate model with common fields."""
    name: str = Field(..., min_length=1, max_length=255, description="Candidate full name")
    phone: str = Field(..., min_length=10, max_length=20, description="Phone number")
    email: EmailStr = Field(..., description="Email address")
    year_of_birth: int = Field(..., ge=1900, le=2010, description="Year of birth")
    gender: Gender = Field(..., description="Gender")
    education: str = Field(..., min_length=1, max_length=500, description="Education background")
    source: str = Field(..., min_length=1, max_length=255, description="Source of candidate")
    expertise_id: int = Field(..., gt=0, description="Expertise area ID")
    field_id: int = Field(..., gt=0, description="Field ID")
    area_id: int = Field(..., gt=0, description="Area ID")
    level_id: int = Field(..., gt=0, description="Level ID")
    headhunter_id: int = Field(..., gt=0, description="Assigned headhunter ID")
    note: Optional[str] = Field(None, max_length=1000, description="Additional notes")

class CandidateCreate(CandidateBase):
    """Schema for creating a new candidate."""
    pass

class CandidateUpdate(BaseModel):
    """Schema for updating a candidate."""
    name: Optional[str] = Field(None, min_length=1, max_length=255, description="Candidate full name")
    phone: Optional[str] = Field(None, min_length=10, max_length=20, description="Phone number")
    email: Optional[EmailStr] = Field(None, description="Email address")
    year_of_birth: Optional[int] = Field(None, ge=1900, le=2010, description="Year of birth")
    gender: Optional[Gender] = Field(None, description="Gender")
    education: Optional[str] = Field(None, min_length=1, max_length=500, description="Education background")
    source: Optional[str] = Field(None, min_length=1, max_length=255, description="Source of candidate")
    expertise_id: Optional[int] = Field(None, gt=0, description="Expertise area ID")
    field_id: Optional[int] = Field(None, gt=0, description="Field ID")
    area_id: Optional[int] = Field(None, gt=0, description="Area ID")
    level_id: Optional[int] = Field(None, gt=0, description="Level ID")
    headhunter_id: Optional[int] = Field(None, gt=0, description="Assigned headhunter ID")
    note: Optional[str] = Field(None, max_length=1000, description="Additional notes")

class CandidateResponse(CandidateBase):
    """Schema for candidate response."""
    candidate_id: int = Field(..., description="Unique candidate ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        from_attributes = True

class CandidateDetailResponse(DataResponse[CandidateResponse]):
    """Response for single candidate operations."""
    pass

class CandidateListResponse(ListResponse[CandidateResponse]):
    """Response for candidate list operations."""
    pass
