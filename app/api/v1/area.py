from fastapi import APIRouter, Depends, HTTPException, Query
import datetime
from app.core.repositories.area_repository import AreaRepository
from app.core.exceptions import NotFoundError
from app.deps import get_area_repository
from app.core.entities.area import Area
from app.schemas import (
    AreaCreate,
    AreaUpdate,
    AreaResponse,
    AreaDetailResponse,
    AreaListResponse,
    ErrorResponse,
)
from app.schemas.utils import create_list_response, entity_to_response_model

router = APIRouter(
    prefix="/areas",
    tags=["areas"],
    responses={
        404: {"model": ErrorResponse, "description": "Area not found"},
        400: {"model": ErrorResponse, "description": "Invalid request data"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    }
)

@router.post("/",
    response_model=AreaDetailResponse,
    status_code=201,
    summary="Create a new area",
    description="Create a new area in the system"
)
async def create_area(
    area_data: AreaCreate,
    area_repo: AreaRepository = Depends(get_area_repository),
):
    """Create a new area."""
    try:
        area = Area(
            area_id=None,
            name=area_data.name,
            created_at=None,
            updated_at=None
        )
        
        created_area = area_repo.create_area(area)
        area_response = entity_to_response_model(created_area, AreaResponse)
        
        return AreaDetailResponse(
            success=True,
            message="Area created successfully",
            data=area_response
        )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/",
    response_model=AreaListResponse,
    summary="Get all areas",
    description="Retrieve a paginated list of all areas"
)
async def get_areas(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Number of items per page"),
    area_repo: AreaRepository = Depends(get_area_repository)
):
    """Get all areas with pagination."""
    try:
        offset = (page - 1) * page_size
        areas = area_repo.get_all_areas(limit=page_size, offset=offset)
        
        # Convert entities to response models
        area_responses = [entity_to_response_model(area, AreaResponse) for area in areas]
        
        # For production, you'd want to get the actual total count
        total = len(areas)  # Simplified for this example
        
        return create_list_response(
            data=area_responses,
            total=total,
            page=page,
            page_size=page_size,
            message="Areas retrieved successfully"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search",
    response_model=AreaListResponse,
    summary="Search areas",
    description="Search areas by name with pagination"
)
async def search_areas(
    query: str = Query(..., min_length=1, description="Search query"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Number of items per page"),
    area_repo: AreaRepository = Depends(get_area_repository)
):
    """Search areas by name."""
    try:
        offset = (page - 1) * page_size
        areas = area_repo.search_areas_by_name(
            name_query=query,
            limit=page_size,
            offset=offset
        )
        
        # Convert entities to response models
        area_responses = [entity_to_response_model(area, AreaResponse) for area in areas]
        
        total = len(areas)  # Simplified for this example
        
        return create_list_response(
            data=area_responses,
            total=total,
            page=page,
            page_size=page_size,
            message=f"Found {total} areas matching '{query}'"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{area_id}",
    response_model=AreaDetailResponse,
    summary="Get area by ID",
    description="Retrieve a specific area by its ID"
)
async def get_area(
    area_id: int,
    area_repo: AreaRepository = Depends(get_area_repository)
):
    """Get an area by ID."""
    try:
        area = area_repo.get_area_by_id(area_id)
        
        if not area:
            raise HTTPException(status_code=404, detail="Area not found")
        
        area_response = entity_to_response_model(area, AreaResponse)
        
        return AreaDetailResponse(
            success=True,
            message="Area retrieved successfully",
            data=area_response
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{area_id}",
    response_model=AreaDetailResponse,
    summary="Update area",
    description="Update an existing area's information"
)
async def update_area(
    area_id: int,
    area_data: AreaUpdate,
    area_repo: AreaRepository = Depends(get_area_repository),
):
    """Update an area."""
    try:
        # Get existing area
        existing_area = area_repo.get_area_by_id(area_id)
        
        if not existing_area:
            raise HTTPException(status_code=404, detail="Area not found")
        
        # Update only provided fields
        update_data = area_data.model_dump(exclude_unset=True)
        
        # Create a new entity with updated data
        from app.core.entities.area import Area
        updated_area = Area(
            area_id=existing_area.area_id,
            name=update_data.get('name', existing_area.name),
            created_at=existing_area.created_at,
            updated_at=datetime.datetime.now(datetime.timezone.utc)
        )
        
        saved_area = area_repo.update_area(updated_area)
        area_response = entity_to_response_model(saved_area, AreaResponse)
        
        return AreaDetailResponse(
            success=True,
            message="Area updated successfully",
            data=area_response
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{area_id}",
    status_code=204,
    summary="Delete area",
    description="Delete an area from the system"
)
async def delete_area(
    area_id: int,
    area_repo: AreaRepository = Depends(get_area_repository)
):
    """Delete an area."""
    try:
        area_repo.delete_area(area_id)
        return None  # 204 No Content
        
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Area not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))