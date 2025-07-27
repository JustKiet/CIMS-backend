from fastapi import APIRouter, Depends, HTTPException, Query
import datetime
from app.core.repositories.expertise_repository import ExpertiseRepository
from app.core.entities.expertise import Expertise
from app.core.exceptions import NotFoundError
from app.deps import get_expertise_repository
from app.schemas import (
    ExpertiseCreate,
    ExpertiseUpdate,
    ExpertiseResponse,
    ExpertiseDetailResponse,
    ExpertiseListResponse,
    ErrorResponse,
)
from app.schemas.utils import create_list_response, entity_to_response_model

router = APIRouter(
    prefix="/expertises",
    tags=["expertises"],
    responses={
        404: {"model": ErrorResponse, "description": "Expertise not found"},
        400: {"model": ErrorResponse, "description": "Invalid request data"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    }
)

@router.post("/",
    response_model=ExpertiseDetailResponse,
    status_code=201,
    summary="Create a new expertise",
    description="Create a new expertise in the system"
)
async def create_expertise(
    expertise_data: ExpertiseCreate,
    expertise_repo: ExpertiseRepository = Depends(get_expertise_repository),
):
    """Create a new expertise."""
    try:
        expertise = Expertise(
            expertise_id=None,
            name=expertise_data.name
        )
        
        created_expertise = expertise_repo.create_expertise(expertise)
        expertise_response = entity_to_response_model(created_expertise, ExpertiseResponse)
        
        return ExpertiseDetailResponse(
            success=True,
            message="Expertise created successfully",
            data=expertise_response
        )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/",
    response_model=ExpertiseListResponse,
    summary="Get all expertises",
    description="Retrieve a paginated list of all expertises"
)
async def get_expertises(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Number of items per page"),
    expertise_repo: ExpertiseRepository = Depends(get_expertise_repository)
):
    """Get all expertises with pagination."""
    try:
        offset = (page - 1) * page_size
        expertises = expertise_repo.get_all_expertises(limit=page_size, offset=offset)
        
        expertise_responses = [entity_to_response_model(expertise, ExpertiseResponse) for expertise in expertises]
        total = len(expertises)
        
        return create_list_response(
            data=expertise_responses,
            total=total,
            page=page,
            page_size=page_size,
            message="Expertises retrieved successfully"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search",
    response_model=ExpertiseListResponse,
    summary="Search expertises",
    description="Search expertises by name with pagination"
)
async def search_expertises(
    query: str = Query(..., min_length=1, description="Search query"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Number of items per page"),
    expertise_repo: ExpertiseRepository = Depends(get_expertise_repository)
):
    """Search expertises by name."""
    try:
        offset = (page - 1) * page_size
        expertises = expertise_repo.search_expertises_by_name(
            name_query=query,
            limit=page_size,
            offset=offset
        )
        
        expertise_responses = [entity_to_response_model(expertise, ExpertiseResponse) for expertise in expertises]
        total = len(expertises)
        
        return create_list_response(
            data=expertise_responses,
            total=total,
            page=page,
            page_size=page_size,
            message=f"Found {total} expertises matching '{query}'"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{expertise_id}",
    response_model=ExpertiseDetailResponse,
    summary="Get expertise by ID",
    description="Retrieve a specific expertise by its ID"
)
async def get_expertise(
    expertise_id: int,
    expertise_repo: ExpertiseRepository = Depends(get_expertise_repository)
):
    """Get an expertise by ID."""
    try:
        expertise = expertise_repo.get_expertise_by_id(expertise_id)
        
        if not expertise:
            raise HTTPException(status_code=404, detail="Expertise not found")
        
        expertise_response = entity_to_response_model(expertise, ExpertiseResponse)
        
        return ExpertiseDetailResponse(
            success=True,
            message="Expertise retrieved successfully",
            data=expertise_response
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{expertise_id}",
    response_model=ExpertiseDetailResponse,
    summary="Update expertise",
    description="Update an existing expertise's information"
)
async def update_expertise(
    expertise_id: int,
    expertise_data: ExpertiseUpdate,
    expertise_repo: ExpertiseRepository = Depends(get_expertise_repository),
):
    """Update an expertise."""
    try:
        existing_expertise = expertise_repo.get_expertise_by_id(expertise_id)
        
        if not existing_expertise:
            raise HTTPException(status_code=404, detail="Expertise not found")
        
        update_data = expertise_data.model_dump(exclude_unset=True)
        
        # Create new entity with updated data
        updated_expertise_entity = Expertise(
            expertise_id=existing_expertise.expertise_id,
            name=update_data.get('name', existing_expertise.name),
            created_at=existing_expertise.created_at,
            updated_at=datetime.datetime.now(datetime.timezone.utc)
        )
        
        updated_expertise = expertise_repo.update_expertise(updated_expertise_entity)
        expertise_response = entity_to_response_model(updated_expertise, ExpertiseResponse)
        
        return ExpertiseDetailResponse(
            success=True,
            message="Expertise updated successfully",
            data=expertise_response
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{expertise_id}",
    status_code=204,
    summary="Delete expertise",
    description="Delete an expertise from the system"
)
async def delete_expertise(
    expertise_id: int,
    expertise_repo: ExpertiseRepository = Depends(get_expertise_repository)
):
    """Delete an expertise."""
    try:
        expertise_repo.delete_expertise(expertise_id)
        return None  # 204 No Content
        
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Expertise not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
