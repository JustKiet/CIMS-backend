from fastapi import APIRouter, Depends, HTTPException, Query
import datetime
from cims.core.repositories.nominee_repository import NomineeRepository
from cims.core.entities.nominee import Nominee
from cims.core.exceptions import NotFoundError
from cims.deps import get_nominee_repository
from cims.schemas import (
    NomineeCreate,
    NomineeUpdate,
    NomineeResponse,
    NomineeDetailResponse,
    NomineeListResponse,
    ErrorResponse,
)
from cims.schemas.utils import create_list_response, entity_to_response_model

router = APIRouter(
    prefix="/nominees",
    tags=["nominees"],
    responses={
        404: {"model": ErrorResponse, "description": "Nominee not found"},
        400: {"model": ErrorResponse, "description": "Invalid request data"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    }
)

@router.post("/",
    response_model=NomineeDetailResponse,
    status_code=201,
    summary="Create a new nominee",
    description="Create a new nominee in the system"
)
async def create_nominee(
    nominee_data: NomineeCreate,
    nominee_repo: NomineeRepository = Depends(get_nominee_repository),
):
    """Create a new nominee."""
    try:
        nominee = Nominee(
            nominee_id=None,
            candidate_id=nominee_data.candidate_id,
            project_id=nominee_data.project_id,
            status=nominee_data.status,
            campaign=nominee_data.campaign,
            years_of_experience=nominee_data.years_of_experience,
            salary_expectation=nominee_data.salary_expectation,
            notice_period=nominee_data.notice_period
        )
        
        created_nominee = nominee_repo.create_nominee(nominee)
        nominee_response = entity_to_response_model(created_nominee, NomineeResponse)
        
        return NomineeDetailResponse(
            success=True,
            message="Nominee created successfully",
            data=nominee_response
        )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/",
    response_model=NomineeListResponse,
    summary="Get all nominees",
    description="Retrieve a paginated list of all nominees"
)
async def get_nominees(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Number of items per page"),
    nominee_repo: NomineeRepository = Depends(get_nominee_repository)
):
    """Get all nominees with pagination."""
    try:
        offset = (page - 1) * page_size
        nominees = nominee_repo.get_all_nominees(limit=page_size, offset=offset)
        
        nominee_responses = [entity_to_response_model(nominee, NomineeResponse) for nominee in nominees]
        total = len(nominees)
        
        return create_list_response(
            data=nominee_responses,
            total=total,
            page=page,
            page_size=page_size,
            message="Nominees retrieved successfully"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search",
    response_model=NomineeListResponse,
    summary="Search nominees",
    description="Search nominees by status with pagination"
)
async def search_nominees(
    query: str = Query(..., min_length=1, description="Search query"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Number of items per page"),
    nominee_repo: NomineeRepository = Depends(get_nominee_repository)
):
    """Search nominees by status."""
    try:
        offset = (page - 1) * page_size
        nominees = nominee_repo.search_nominees_by_status(
            status_query=query,
            limit=page_size,
            offset=offset
        )
        
        nominee_responses = [entity_to_response_model(nominee, NomineeResponse) for nominee in nominees]
        total = len(nominees)
        
        return create_list_response(
            data=nominee_responses,
            total=total,
            page=page,
            page_size=page_size,
            message=f"Found {total} nominees matching status '{query}'"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/by-candidate/{candidate_id}",
    response_model=NomineeListResponse,
    summary="Get nominees by candidate ID",
    description="Retrieve all nominees for a specific candidate"
)
async def get_nominees_by_candidate(
    candidate_id: int,
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Number of items per page"),
    nominee_repo: NomineeRepository = Depends(get_nominee_repository)
):
    """Get nominees by candidate ID."""
    try:
        offset = (page - 1) * page_size
        nominees = nominee_repo.get_nominees_by_candidate_id(
            candidate_id=candidate_id,
            limit=page_size,
            offset=offset
        )
        
        nominee_responses = [entity_to_response_model(nominee, NomineeResponse) for nominee in nominees]
        total = len(nominees)
        
        return create_list_response(
            data=nominee_responses,
            total=total,
            page=page,
            page_size=page_size,
            message=f"Found {total} nominees for candidate {candidate_id}"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/by-project/{project_id}",
    response_model=NomineeListResponse,
    summary="Get nominees by project ID",
    description="Retrieve all nominees for a specific project"
)
async def get_nominees_by_project(
    project_id: int,
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Number of items per page"),
    nominee_repo: NomineeRepository = Depends(get_nominee_repository)
):
    """Get nominees by project ID."""
    try:
        offset = (page - 1) * page_size
        nominees = nominee_repo.get_nominees_by_project_id(
            project_id=project_id,
            limit=page_size,
            offset=offset
        )
        
        nominee_responses = [entity_to_response_model(nominee, NomineeResponse) for nominee in nominees]
        total = len(nominees)
        
        return create_list_response(
            data=nominee_responses,
            total=total,
            page=page,
            page_size=page_size,
            message=f"Found {total} nominees for project {project_id}"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{nominee_id}",
    response_model=NomineeDetailResponse,
    summary="Get nominee by ID",
    description="Retrieve a specific nominee by their ID"
)
async def get_nominee(
    nominee_id: int,
    nominee_repo: NomineeRepository = Depends(get_nominee_repository)
):
    """Get a nominee by ID."""
    try:
        nominee = nominee_repo.get_nominee_by_id(nominee_id)
        
        if not nominee:
            raise HTTPException(status_code=404, detail="Nominee not found")
        
        nominee_response = entity_to_response_model(nominee, NomineeResponse)
        
        return NomineeDetailResponse(
            success=True,
            message="Nominee retrieved successfully",
            data=nominee_response
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{nominee_id}",
    response_model=NomineeDetailResponse,
    summary="Update nominee",
    description="Update an existing nominee's information"
)
async def update_nominee(
    nominee_id: int,
    nominee_data: NomineeUpdate,
    nominee_repo: NomineeRepository = Depends(get_nominee_repository),
):
    """Update a nominee."""
    try:
        existing_nominee = nominee_repo.get_nominee_by_id(nominee_id)
        
        if not existing_nominee:
            raise HTTPException(status_code=404, detail="Nominee not found")
        
        update_data = nominee_data.model_dump(exclude_unset=True)
        
        # Create new entity with updated data
        updated_nominee_entity = Nominee(
            nominee_id=existing_nominee.nominee_id,
            campaign=update_data.get('campaign', existing_nominee.campaign),
            status=update_data.get('status', existing_nominee.status),
            years_of_experience=update_data.get('years_of_experience', existing_nominee.years_of_experience),
            salary_expectation=update_data.get('salary_expectation', existing_nominee.salary_expectation),
            notice_period=update_data.get('notice_period', existing_nominee.notice_period),
            candidate_id=update_data.get('candidate_id', existing_nominee.candidate_id),
            project_id=update_data.get('project_id', existing_nominee.project_id),
            created_at=existing_nominee.created_at,
            updated_at=datetime.datetime.now(datetime.timezone.utc)
        )
        
        updated_nominee = nominee_repo.update_nominee(updated_nominee_entity)
        nominee_response = entity_to_response_model(updated_nominee, NomineeResponse)
        
        return NomineeDetailResponse(
            success=True,
            message="Nominee updated successfully",
            data=nominee_response
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{nominee_id}",
    status_code=204,
    summary="Delete nominee",
    description="Delete a nominee from the system"
)
async def delete_nominee(
    nominee_id: int,
    nominee_repo: NomineeRepository = Depends(get_nominee_repository)
):
    """Delete a nominee."""
    try:
        nominee_repo.delete_nominee(nominee_id)
        return None  # 204 No Content
        
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Nominee not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
