"""
Nominee API schemas for requests and responses.
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from cims.core.entities.nominee import NomineeStatus
from cims.schemas.base import DataResponse, ListResponse

class NomineeBase(BaseModel):
    """Base nominee model with common fields."""
    candidate_id: int = Field(..., gt=0, description="Candidate ID")
    project_id: int = Field(..., gt=0, description="Project ID")
    status: NomineeStatus = Field(..., description="Nominee status")
    campaign: str = Field(..., max_length=255, description="Campaign name")
    years_of_experience: int = Field(..., ge=0, description="Years of experience")
    salary_expectation: float = Field(..., ge=0, description="Expected salary")
    notice_period: int = Field(..., ge=0, description="Notice period in days")

class NomineeCreate(NomineeBase):
    """Schema for creating a new nominee."""
    pass

class NomineeUpdate(BaseModel):
    """Schema for updating a nominee."""
    candidate_id: Optional[int] = Field(None, gt=0, description="Candidate ID")
    project_id: Optional[int] = Field(None, gt=0, description="Project ID")
    status: Optional[NomineeStatus] = Field(None, description="Nominee status")
    campaign: Optional[str] = Field(None, max_length=255, description="Campaign name")
    years_of_experience: Optional[int] = Field(None, ge=0, description="Years of experience")
    salary_expectation: Optional[float] = Field(None, ge=0, description="Expected salary")
    notice_period: Optional[int] = Field(None, ge=0, description="Notice period in days")

class NomineeResponse(NomineeBase):
    """Schema for nominee response."""
    nominee_id: int = Field(..., description="Unique nominee ID")
    nominee_name: Optional[str] = Field(None, max_length=255, description="Nominee name")
    project_name: Optional[str] = Field(None, max_length=255, description="Project name")
    headhunter_name: Optional[str] = Field(None, max_length=255, description="Headhunter name")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        from_attributes = True

class NomineeDetailResponse(DataResponse[NomineeResponse]):
    """Response for single nominee operations."""
    pass

class NomineeListResponse(ListResponse[NomineeResponse]):
    """Response for nominee list operations."""
    pass
