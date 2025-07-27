from fastapi import APIRouter, Depends, HTTPException, Query
import datetime
from app.core.repositories.candidate_repository import CandidateRepository
from app.core.entities.candidate import Candidate
from app.core.exceptions import NotFoundError
from app.deps import get_candidate_repository
from app.schemas import (
    CandidateCreate,
    CandidateUpdate,
    CandidateResponse,
    CandidateDetailResponse,
    CandidateListResponse,
    ErrorResponse,
)
from app.schemas.utils import create_list_response, entity_to_response_model

router = APIRouter(
    prefix="/candidates",
    tags=["candidates"],
    responses={
        404: {"model": ErrorResponse, "description": "Candidate not found"},
        400: {"model": ErrorResponse, "description": "Invalid request data"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    }
)

@router.post("/",
    response_model=CandidateDetailResponse,
    status_code=201,
    summary="Create a new candidate",
    description="Create a new candidate in the system"
)
async def create_candidate(
    candidate_data: CandidateCreate,
    candidate_repo: CandidateRepository = Depends(get_candidate_repository),
):
    """Create a new candidate."""
    try:
        candidate = Candidate(
            candidate_id=None,
            name=candidate_data.name,
            phone=candidate_data.phone,
            email=str(candidate_data.email),
            year_of_birth=candidate_data.year_of_birth,
            gender=candidate_data.gender,
            education=candidate_data.education,
            source=candidate_data.source,
            expertise_id=candidate_data.expertise_id,
            field_id=candidate_data.field_id,
            area_id=candidate_data.area_id,
            level_id=candidate_data.level_id,
            headhunter_id=candidate_data.headhunter_id,
            note=candidate_data.note,
            created_at=None,
            updated_at=None
        )
        
        created_candidate = candidate_repo.create_candidate(candidate)
        candidate_response = entity_to_response_model(created_candidate, CandidateResponse)
        
        return CandidateDetailResponse(
            success=True,
            message="Candidate created successfully",
            data=candidate_response
        )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/",
    response_model=CandidateListResponse,
    summary="Get all candidates",
    description="Retrieve a paginated list of all candidates"
)
async def get_candidates(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Number of items per page"),
    candidate_repo: CandidateRepository = Depends(get_candidate_repository)
):
    """Get all candidates with pagination."""
    try:
        offset = (page - 1) * page_size
        candidates = candidate_repo.get_all_candidates(limit=page_size, offset=offset)
        
        candidate_responses = [entity_to_response_model(candidate, CandidateResponse) for candidate in candidates]
        total = len(candidates)
        
        return create_list_response(
            data=candidate_responses,
            total=total,
            page=page,
            page_size=page_size,
            message="Candidates retrieved successfully"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search",
    response_model=CandidateListResponse,
    summary="Search candidates",
    description="Search candidates by name with pagination"
)
async def search_candidates(
    query: str = Query(..., min_length=1, description="Search query"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Number of items per page"),
    candidate_repo: CandidateRepository = Depends(get_candidate_repository)
):
    """Search candidates by name."""
    try:
        offset = (page - 1) * page_size
        candidates = candidate_repo.search_candidates_by_name(
            name_query=query,
            limit=page_size,
            offset=offset
        )
        
        candidate_responses = [entity_to_response_model(candidate, CandidateResponse) for candidate in candidates]
        total = len(candidates)
        
        return create_list_response(
            data=candidate_responses,
            total=total,
            page=page,
            page_size=page_size,
            message=f"Found {total} candidates matching '{query}'"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{candidate_id}",
    response_model=CandidateDetailResponse,
    summary="Get candidate by ID",
    description="Retrieve a specific candidate by their ID"
)
async def get_candidate(
    candidate_id: int,
    candidate_repo: CandidateRepository = Depends(get_candidate_repository)
):
    """Get a candidate by ID."""
    try:
        candidate = candidate_repo.get_candidate_by_id(candidate_id)
        
        if not candidate:
            raise HTTPException(status_code=404, detail="Candidate not found")
        
        candidate_response = entity_to_response_model(candidate, CandidateResponse)
        
        return CandidateDetailResponse(
            success=True,
            message="Candidate retrieved successfully",
            data=candidate_response
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{candidate_id}",
    response_model=CandidateDetailResponse,
    summary="Update candidate",
    description="Update an existing candidate's information"
)
async def update_candidate(
    candidate_id: int,
    candidate_data: CandidateUpdate,
    candidate_repo: CandidateRepository = Depends(get_candidate_repository),
):
    """Update a candidate."""
    try:
        existing_candidate = candidate_repo.get_candidate_by_id(candidate_id)
        
        if not existing_candidate:
            raise HTTPException(status_code=404, detail="Candidate not found")
        
        update_data = candidate_data.model_dump(exclude_unset=True)
        
        # Create new entity with updated data
        updated_candidate_entity = Candidate(
            candidate_id=existing_candidate.candidate_id,
            name=update_data.get('name', existing_candidate.name),
            phone=update_data.get('phone', existing_candidate.phone),
            email=update_data.get('email', existing_candidate.email),
            year_of_birth=update_data.get('year_of_birth', existing_candidate.year_of_birth),
            gender=update_data.get('gender', existing_candidate.gender),
            education=update_data.get('education', existing_candidate.education),
            source=update_data.get('source', existing_candidate.source),
            expertise_id=update_data.get('expertise_id', existing_candidate.expertise_id),
            field_id=update_data.get('field_id', existing_candidate.field_id),
            area_id=update_data.get('area_id', existing_candidate.area_id),
            level_id=update_data.get('level_id', existing_candidate.level_id),
            headhunter_id=update_data.get('headhunter_id', existing_candidate.headhunter_id),
            note=update_data.get('note', existing_candidate.note),
            created_at=existing_candidate.created_at,
            updated_at=datetime.datetime.now(datetime.timezone.utc)
        )
        
        updated_candidate = candidate_repo.update_candidate(updated_candidate_entity)
        candidate_response = entity_to_response_model(updated_candidate, CandidateResponse)
        
        return CandidateDetailResponse(
            success=True,
            message="Candidate updated successfully",
            data=candidate_response
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{candidate_id}",
    status_code=204,
    summary="Delete candidate",
    description="Delete a candidate from the system"
)
async def delete_candidate(
    candidate_id: int,
    candidate_repo: CandidateRepository = Depends(get_candidate_repository)
):
    """Delete a candidate."""
    try:
        candidate_repo.delete_candidate(candidate_id)
        return None  # 204 No Content
        
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Candidate not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))