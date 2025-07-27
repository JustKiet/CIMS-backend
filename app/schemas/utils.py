"""
Utility functions for schema operations and API helpers.
"""
from typing import List, TypeVar, Any, Type
from math import ceil
from app.schemas.base import PaginationMeta, ListResponse

T = TypeVar('T')
ResponseType = TypeVar('ResponseType')

def create_pagination_meta(
    total: int,
    page: int,
    page_size: int
) -> PaginationMeta:
    """
    Create pagination metadata.
    
    Args:
        total: Total number of items
        page: Current page number
        page_size: Number of items per page
        
    Returns:
        PaginationMeta object with calculated values
    """
    total_pages = ceil(total / page_size) if page_size > 0 else 0
    has_next = page < total_pages
    has_previous = page > 1
    
    return PaginationMeta(
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        has_next=has_next,
        has_previous=has_previous
    )

def create_list_response(
    data: List[T],
    total: int,
    page: int,
    page_size: int,
    message: str = "Data retrieved successfully"
) -> ListResponse[T]:
    """
    Create a standardized list response with pagination.
    
    Args:
        data: List of items to return
        total: Total number of items available
        page: Current page number
        page_size: Number of items per page
        message: Success message
        
    Returns:
        ListResponse object with data and pagination metadata
    """
    pagination = create_pagination_meta(total, page, page_size)
    
    return ListResponse(
        success=True,
        message=message,
        data=data,
        pagination=pagination
    )

def validate_pagination_params(page: int, page_size: int) -> tuple[int, int]:
    """
    Validate and normalize pagination parameters.
    
    Args:
        page: Page number
        page_size: Page size
        
    Returns:
        Tuple of (normalized_page, normalized_page_size)
        
    Raises:
        ValueError: If parameters are invalid
    """
    if page < 1:
        raise ValueError("Page number must be >= 1")
    
    if page_size < 1:
        raise ValueError("Page size must be >= 1")
    
    if page_size > 100:
        raise ValueError("Page size cannot exceed 100")
        
    return page, page_size

def calculate_offset(page: int, page_size: int) -> int:
    """
    Calculate database offset from page and page_size.
    
    Args:
        page: Page number (1-based)
        page_size: Number of items per page
        
    Returns:
        Database offset (0-based)
    """
    return (page - 1) * page_size

def entity_to_response_model(entity: Any, response_class: Type[ResponseType]) -> ResponseType:
    """
    Convert a domain entity to a response model.
    
    Args:
        entity: Domain entity object
        response_class: Pydantic response model class
        
    Returns:
        Response model instance
    """
    if hasattr(entity, 'to_dict'):
        entity_dict = entity.to_dict()
    else:
        # Fallback to __dict__ if to_dict is not available
        entity_dict = entity.__dict__
    
    return response_class(**entity_dict)
