from fastapi import APIRouter, Depends, HTTPException, Query
import datetime
from app.core.repositories.headhunter_repository import HeadhunterRepository
from app.core.entities.headhunter import Headhunter
from app.core.exceptions import NotFoundError
from app.deps import get_headhunter_repository
from app.schemas import (
    HeadhunterCreate,
    HeadhunterUpdate,
    HeadhunterResponse,
    HeadhunterDetailResponse,
    HeadhunterListResponse,
    ErrorResponse,
)
from app.schemas.utils import create_list_response, entity_to_response_model

router = APIRouter(
    prefix="/headhunters",
    tags=["headhunters"],
    responses={
        404: {"model": ErrorResponse, "description": "Headhunter not found"},
        400: {"model": ErrorResponse, "description": "Invalid request data"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    }
)

@router.post("/",
    response_model=HeadhunterDetailResponse,
    status_code=201,
    summary="Create a new headhunter",
    description="Create a new headhunter in the system"
)
async def create_headhunter(
    headhunter_data: HeadhunterCreate,
    headhunter_repo: HeadhunterRepository = Depends(get_headhunter_repository),
):
    """Create a new headhunter."""
    try:
        headhunter = Headhunter(
            headhunter_id=None,
            name=headhunter_data.name,
            phone=headhunter_data.phone,
            email=str(headhunter_data.email),
            hashed_password=headhunter_data.password,  # In production, this should be hashed
            role=headhunter_data.role or "HEADHUNTER",
            area_id=headhunter_data.area_id or 1,  # Default area_id
            created_at=None,
            updated_at=None
        )
        
        created_headhunter = headhunter_repo.create_headhunter(headhunter)
        headhunter_response = entity_to_response_model(created_headhunter, HeadhunterResponse)
        
        return HeadhunterDetailResponse(
            success=True,
            message="Headhunter created successfully",
            data=headhunter_response
        )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/",
    response_model=HeadhunterListResponse,
    summary="Get all headhunters",
    description="Retrieve a paginated list of all headhunters"
)
async def get_headhunters(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Number of items per page"),
    headhunter_repo: HeadhunterRepository = Depends(get_headhunter_repository)
):
    """Get all headhunters with pagination."""
    try:
        offset = (page - 1) * page_size
        headhunters = headhunter_repo.get_all_headhunters(limit=page_size, offset=offset)
        
        headhunter_responses = [entity_to_response_model(headhunter, HeadhunterResponse) for headhunter in headhunters]
        total = len(headhunters)
        
        return create_list_response(
            data=headhunter_responses,
            total=total,
            page=page,
            page_size=page_size,
            message="Headhunters retrieved successfully"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search",
    response_model=HeadhunterListResponse,
    summary="Search headhunters",
    description="Search headhunters by name with pagination"
)
async def search_headhunters(
    query: str = Query(..., min_length=1, description="Search query"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Number of items per page"),
    headhunter_repo: HeadhunterRepository = Depends(get_headhunter_repository)
):
    """Search headhunters by name."""
    try:
        offset = (page - 1) * page_size
        headhunters = headhunter_repo.search_headhunters_by_name(
            name_query=query,
            limit=page_size,
            offset=offset
        )
        
        headhunter_responses = [entity_to_response_model(headhunter, HeadhunterResponse) for headhunter in headhunters]
        total = len(headhunters)
        
        return create_list_response(
            data=headhunter_responses,
            total=total,
            page=page,
            page_size=page_size,
            message=f"Found {total} headhunters matching '{query}'"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/by-email/{email}",
    response_model=HeadhunterDetailResponse,
    summary="Get headhunter by email",
    description="Retrieve a specific headhunter by their email address"
)
async def get_headhunter_by_email(
    email: str,
    headhunter_repo: HeadhunterRepository = Depends(get_headhunter_repository)
):
    """Get a headhunter by email."""
    try:
        headhunter = headhunter_repo.get_headhunter_by_email(email)
        
        if not headhunter:
            raise HTTPException(status_code=404, detail="Headhunter not found")
        
        headhunter_response = entity_to_response_model(headhunter, HeadhunterResponse)
        
        return HeadhunterDetailResponse(
            success=True,
            message="Headhunter retrieved successfully",
            data=headhunter_response
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{headhunter_id}",
    response_model=HeadhunterDetailResponse,
    summary="Get headhunter by ID",
    description="Retrieve a specific headhunter by their ID"
)
async def get_headhunter(
    headhunter_id: int,
    headhunter_repo: HeadhunterRepository = Depends(get_headhunter_repository)
):
    """Get a headhunter by ID."""
    try:
        headhunter = headhunter_repo.get_headhunter_by_id(headhunter_id)
        
        if not headhunter:
            raise HTTPException(status_code=404, detail="Headhunter not found")
        
        headhunter_response = entity_to_response_model(headhunter, HeadhunterResponse)
        
        return HeadhunterDetailResponse(
            success=True,
            message="Headhunter retrieved successfully",
            data=headhunter_response
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{headhunter_id}",
    response_model=HeadhunterDetailResponse,
    summary="Update headhunter",
    description="Update an existing headhunter's information"
)
async def update_headhunter(
    headhunter_id: int,
    headhunter_data: HeadhunterUpdate,
    headhunter_repo: HeadhunterRepository = Depends(get_headhunter_repository),
):
    """Update a headhunter."""
    try:
        existing_headhunter = headhunter_repo.get_headhunter_by_id(headhunter_id)
        
        if not existing_headhunter:
            raise HTTPException(status_code=404, detail="Headhunter not found")
        
        update_data = headhunter_data.model_dump(exclude_unset=True)
        
        # Create new entity with updated data
        updated_headhunter_entity = Headhunter(
            headhunter_id=existing_headhunter.headhunter_id,
            name=update_data.get('name', existing_headhunter.name),
            phone=update_data.get('phone', existing_headhunter.phone),
            email=update_data.get('email', existing_headhunter.email),
            hashed_password=update_data.get('hashed_password', existing_headhunter.hashed_password),
            role=update_data.get('role', existing_headhunter.role),
            area_id=update_data.get('area_id', existing_headhunter.area_id),
            created_at=existing_headhunter.created_at,
            updated_at=datetime.datetime.now(datetime.timezone.utc)
        )
        
        updated_headhunter = headhunter_repo.update_headhunter(updated_headhunter_entity)
        headhunter_response = entity_to_response_model(updated_headhunter, HeadhunterResponse)
        
        return HeadhunterDetailResponse(
            success=True,
            message="Headhunter updated successfully",
            data=headhunter_response
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{headhunter_id}",
    status_code=204,
    summary="Delete headhunter",
    description="Delete a headhunter from the system"
)
async def delete_headhunter(
    headhunter_id: int,
    headhunter_repo: HeadhunterRepository = Depends(get_headhunter_repository)
):
    """Delete a headhunter."""
    try:
        headhunter_repo.delete_headhunter(headhunter_id)
        return None  # 204 No Content
        
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Headhunter not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
