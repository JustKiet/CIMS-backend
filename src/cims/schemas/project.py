"""
Project API schemas for requests and responses.
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date
from cims.schemas.base import DataResponse, ListResponse
from cims.core.entities.project import ProjectType, ProjectStatus

class ProjectBase(BaseModel):
    """Base project model with common fields."""
    name: Optional[str] = Field(None, min_length=1, max_length=255, description="Project name")
    description: Optional[str] = Field(None, max_length=2000, description="Project description")
    start_date: date = Field(..., description="Project start date")
    end_date: date = Field(..., description="Project end date")
    budget: float = Field(..., ge=0, description="Project budget")
    budget_currency: str = Field(..., max_length=3, description="Currency of the project budget")
    type: ProjectType = Field(..., description="Type of the project")
    required_recruits: int = Field(..., ge=0, description="Number of recruits required for the project")
    recruited: int = Field(..., ge=0, description="Number of recruits already recruited")
    status: ProjectStatus = Field(..., description="Current status of the project")
    customer_id: int = Field(..., gt=0, description="Customer ID")
    expertise_id: int = Field(..., gt=0, description="Expertise ID")
    area_id: int = Field(..., gt=0, description="Area ID")
    level_id: int = Field(..., gt=0, description="Level ID")

class ProjectCreate(ProjectBase):
    """Schema for creating a new project."""
    pass

class ProjectUpdate(BaseModel):
    """Schema for updating a project."""
    description: Optional[str] = Field(None, max_length=2000, description="Project description")
    start_date: Optional[date] = Field(None, description="Project start date")
    end_date: Optional[date] = Field(None, description="Project end date")
    budget: Optional[float] = Field(None, ge=0, description="Project budget")
    budget_currency: Optional[str] = Field(None, max_length=3, description="Currency of the project budget")
    type: Optional[ProjectType] = Field(None, description="Type of the project")
    required_recruits: Optional[int] = Field(1, ge=0, description="Number of recruits required for the project")
    recruited: Optional[int] = Field(0, ge=0, description="Number of recruits already recruited")
    status: Optional[ProjectStatus] = Field(None, description="Current status of the project")
    customer_id: Optional[int] = Field(None, gt=0, description="Customer ID")
    expertise_id: Optional[int] = Field(None, gt=0, description="Expertise ID")
    area_id: Optional[int] = Field(None, gt=0, description="Area ID")
    level_id: Optional[int] = Field(None, gt=0, description="Level ID")

class ProjectResponse(ProjectBase):
    """Schema for project response."""
    project_id: int = Field(..., description="Unique project ID")
    customer_name: str = Field("", description="Name of the customer")
    expertise_name: str = Field("", description="Name of the expertise")
    area_name: str = Field("", description="Name of the area")
    level_name: str = Field("", description="Name of the level")
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
