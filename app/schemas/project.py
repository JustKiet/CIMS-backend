"""
Project API schemas for requests and responses.
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date
from app.schemas.base import DataResponse, ListResponse

class ProjectBase(BaseModel):
    """Base project model with common fields."""
    name: str = Field(..., min_length=1, max_length=255, description="Project name")
    customer_id: int = Field(..., gt=0, description="Customer ID")
    description: Optional[str] = Field(None, max_length=2000, description="Project description")
    status: str = Field(..., max_length=50, description="Project status")
    start_date: Optional[date] = Field(None, description="Project start date")
    end_date: Optional[date] = Field(None, description="Project end date")
    budget: Optional[float] = Field(None, ge=0, description="Project budget")

class ProjectCreate(ProjectBase):
    """Schema for creating a new project."""
    pass

class ProjectUpdate(BaseModel):
    """Schema for updating a project."""
    name: Optional[str] = Field(None, min_length=1, max_length=255, description="Project name")
    customer_id: Optional[int] = Field(None, gt=0, description="Customer ID")
    description: Optional[str] = Field(None, max_length=2000, description="Project description")
    status: Optional[str] = Field(None, max_length=50, description="Project status")
    start_date: Optional[date] = Field(None, description="Project start date")
    end_date: Optional[date] = Field(None, description="Project end date")
    budget: Optional[float] = Field(None, ge=0, description="Project budget")

class ProjectResponse(ProjectBase):
    """Schema for project response."""
    project_id: int = Field(..., description="Unique project ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        from_attributes = True

class ProjectDetailResponse(DataResponse[ProjectResponse]):
    """Response for single project operations."""
    pass

class ProjectListResponse(ListResponse[ProjectResponse]):
    """Response for project list operations."""
    pass
