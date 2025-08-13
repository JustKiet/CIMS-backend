"""
Base schemas for common API patterns and responses.
"""
from pydantic import BaseModel, Field
from typing import Generic, TypeVar, List, Optional, Dict, Any
from datetime import datetime, timezone

T = TypeVar('T')

class BaseResponse(BaseModel):
    """Base response model with common fields."""
    success: bool = True
    message: str = "Operation completed successfully"
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class DataResponse(BaseResponse, Generic[T]):
    """Response with data payload."""
    data: T

class ListResponse(BaseResponse, Generic[T]):
    """Response for paginated list operations."""
    data: List[T]
    pagination: "PaginationMeta"

class PaginationMeta(BaseModel):
    """Pagination metadata."""
    total: int = Field(..., description="Total number of items")
    page: int = Field(..., description="Current page number", ge=1)
    page_size: int = Field(..., description="Number of items per page", ge=1, le=100)
    total_pages: int = Field(..., description="Total number of pages")
    has_next: bool = Field(..., description="Whether there is a next page")
    has_previous: bool = Field(..., description="Whether there is a previous page")

class ErrorResponse(BaseModel):
    """Error response model."""
    success: bool = False
    message: str
    error_code: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class PaginationParams(BaseModel):
    """Common pagination parameters."""
    page: int = Field(1, ge=1, description="Page number")
    page_size: int = Field(20, ge=1, le=100, description="Number of items per page")
    
    @property
    def offset(self) -> int:
        """Calculate offset for database queries."""
        return (self.page - 1) * self.page_size
    
    @property
    def limit(self) -> int:
        """Get limit for database queries."""
        return self.page_size

class SearchParams(PaginationParams):
    """Search parameters with pagination."""
    query: str = Field(..., min_length=1, max_length=255, description="Search query")

# Update forward references
ListResponse.model_rebuild()
