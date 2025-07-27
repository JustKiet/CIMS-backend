from fastapi import APIRouter, Depends, HTTPException, Query
import datetime
from app.core.repositories.level_repository import LevelRepository
from app.core.entities.level import Level
from app.core.exceptions import NotFoundError
from app.deps import get_level_repository
from app.schemas import (
    LevelCreate,
    LevelUpdate,
    LevelResponse,
    LevelDetailResponse,
    LevelListResponse,
    ErrorResponse,
)
from app.schemas.utils import create_list_response, entity_to_response_model

router = APIRouter(
    prefix="/levels",
    tags=["levels"],
    responses={
        404: {"model": ErrorResponse, "description": "Level not found"},
        400: {"model": ErrorResponse, "description": "Invalid request data"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    }
)

@router.post("/",
    response_model=LevelDetailResponse,
    status_code=201,
    summary="Create a new level",
    description="Create a new level in the system"
)
async def create_level(
    level_data: LevelCreate,
    level_repo: LevelRepository = Depends(get_level_repository),
):
    """Create a new level."""
    try:
        level = Level(
            level_id=None,
            name=level_data.name,
            created_at=None,
            updated_at=None
        )
        
        created_level = level_repo.create_level(level)
        level_response = entity_to_response_model(created_level, LevelResponse)
        
        return LevelDetailResponse(
            success=True,
            message="Level created successfully",
            data=level_response
        )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/",
    response_model=LevelListResponse,
    summary="Get all levels",
    description="Retrieve a paginated list of all levels"
)
async def get_levels(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Number of items per page"),
    level_repo: LevelRepository = Depends(get_level_repository)
):
    """Get all levels with pagination."""
    try:
        offset = (page - 1) * page_size
        levels = level_repo.get_all_levels(limit=page_size, offset=offset)
        
        level_responses = [entity_to_response_model(level, LevelResponse) for level in levels]
        total = len(levels)
        
        return create_list_response(
            data=level_responses,
            total=total,
            page=page,
            page_size=page_size,
            message="Levels retrieved successfully"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search",
    response_model=LevelListResponse,
    summary="Search levels",
    description="Search levels by name with pagination"
)
async def search_levels(
    query: str = Query(..., min_length=1, description="Search query"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Number of items per page"),
    level_repo: LevelRepository = Depends(get_level_repository)
):
    """Search levels by name."""
    try:
        offset = (page - 1) * page_size
        levels = level_repo.search_levels_by_name(
            name_query=query,
            limit=page_size,
            offset=offset
        )
        
        level_responses = [entity_to_response_model(level, LevelResponse) for level in levels]
        total = len(levels)
        
        return create_list_response(
            data=level_responses,
            total=total,
            page=page,
            page_size=page_size,
            message=f"Found {total} levels matching '{query}'"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{level_id}",
    response_model=LevelDetailResponse,
    summary="Get level by ID",
    description="Retrieve a specific level by its ID"
)
async def get_level(
    level_id: int,
    level_repo: LevelRepository = Depends(get_level_repository)
):
    """Get a level by ID."""
    try:
        level = level_repo.get_level_by_id(level_id)
        
        if not level:
            raise HTTPException(status_code=404, detail="Level not found")
        
        level_response = entity_to_response_model(level, LevelResponse)
        
        return LevelDetailResponse(
            success=True,
            message="Level retrieved successfully",
            data=level_response
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{level_id}",
    response_model=LevelDetailResponse,
    summary="Update level",
    description="Update an existing level's information"
)
async def update_level(
    level_id: int,
    level_data: LevelUpdate,
    level_repo: LevelRepository = Depends(get_level_repository),
):
    """Update a level."""
    try:
        existing_level = level_repo.get_level_by_id(level_id)
        
        if not existing_level:
            raise HTTPException(status_code=404, detail="Level not found")
        
        update_data = level_data.model_dump(exclude_unset=True)
        
        # Create new entity with updated data
        updated_level_entity = Level(
            level_id=existing_level.level_id,
            name=update_data.get('name', existing_level.name),
            created_at=existing_level.created_at,
            updated_at=datetime.datetime.now(datetime.timezone.utc)
        )
        
        updated_level = level_repo.update_level(updated_level_entity)
        level_response = entity_to_response_model(updated_level, LevelResponse)
        
        return LevelDetailResponse(
            success=True,
            message="Level updated successfully",
            data=level_response
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{level_id}",
    status_code=204,
    summary="Delete level",
    description="Delete a level from the system"
)
async def delete_level(
    level_id: int,
    level_repo: LevelRepository = Depends(get_level_repository)
):
    """Delete a level."""
    try:
        level_repo.delete_level(level_id)
        return None  # 204 No Content
        
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Level not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
