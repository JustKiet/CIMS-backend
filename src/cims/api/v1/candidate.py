from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
import datetime

from cims.core.repositories.candidate_repository import CandidateRepository
from cims.core.repositories.expertise_repository import ExpertiseRepository
from cims.core.repositories.field_repository import FieldRepository
from cims.core.repositories.area_repository import AreaRepository
from cims.core.repositories.level_repository import LevelRepository
from cims.core.repositories.headhunter_repository import HeadhunterRepository
from cims.core.entities.candidate import Candidate
from cims.core.exceptions import NotFoundError
from cims.deps import (
    get_candidate_repository,
    get_expertise_repository,
    get_field_repository,
    get_area_repository,
    get_level_repository,
    get_headhunter_repository
)
from cims.schemas import (
    CandidateCreate,
    CandidateUpdate,
    CandidateResponse,
    CandidateDetailResponse,
    CandidateListResponse,
    ErrorResponse,
)
from cims.schemas.utils import create_list_response, entity_to_response_model

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
    candidate_repo: CandidateRepository = Depends(get_candidate_repository),
    expertise_repo: ExpertiseRepository = Depends(get_expertise_repository),
    field_repo: FieldRepository = Depends(get_field_repository),
    area_repo: AreaRepository = Depends(get_area_repository),
    level_repo: LevelRepository = Depends(get_level_repository),
    headhunter_repo: HeadhunterRepository = Depends(get_headhunter_repository)
):
    """Get all candidates with pagination."""
    try:
        offset = (page - 1) * page_size
        candidates = candidate_repo.get_all_candidates(limit=page_size, offset=offset)
        total = candidate_repo.count_all_candidates()

        candidate_responses = [entity_to_response_model(candidate, CandidateResponse) for candidate in candidates]

        if candidate_responses:
            expertise_ids = {c.expertise_id for c in candidates}
            field_ids = {c.field_id for c in candidates}
            area_ids = {c.area_id for c in candidates}
            level_ids = {c.level_id for c in candidates}
            headhunter_ids = {c.headhunter_id for c in candidates}

            expertises = expertise_repo.get_expertises_by_ids(list(expertise_ids))
            fields = field_repo.get_fields_by_ids(list(field_ids))
            areas = area_repo.get_areas_by_ids(list(area_ids))
            levels = level_repo.get_levels_by_ids(list(level_ids))
            headhunters = headhunter_repo.get_headhunters_by_ids(list(headhunter_ids))

            expertise_map = {e.expertise_id: e.name for e in expertises}
            field_map = {f.field_id: f.name for f in fields}
            area_map = {a.area_id: a.name for a in areas}
            level_map = {l.level_id: l.name for l in levels}
            headhunter_map = {h.headhunter_id: h.name for h in headhunters}

            for candidate_response in candidate_responses:
                candidate_response.expertise_name = expertise_map.get(candidate_response.expertise_id)
                candidate_response.field_name = field_map.get(candidate_response.field_id)
                candidate_response.area_name = area_map.get(candidate_response.area_id)
                candidate_response.level_name = level_map.get(candidate_response.level_id)
                candidate_response.headhunter_name = headhunter_map.get(candidate_response.headhunter_id)

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
    query: str = Query("", description="Search query"),
    expertise_id: Optional[int] = Query(None, description="Expertise ID filter"),
    field_id: Optional[int] = Query(None, description="Field ID filter"),
    area_id: Optional[int] = Query(None, description="Area ID filter"),
    level_id: Optional[int] = Query(None, description="Level ID filter"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Number of items per page"),
    candidate_repo: CandidateRepository = Depends(get_candidate_repository),
    expertise_repo: ExpertiseRepository = Depends(get_expertise_repository),
    field_repo: FieldRepository = Depends(get_field_repository),
    area_repo: AreaRepository = Depends(get_area_repository),
    level_repo: LevelRepository = Depends(get_level_repository),
    headhunter_repo: HeadhunterRepository = Depends(get_headhunter_repository)
):
    """Search candidates by name and/or filters."""
    try:
        # Validate that at least one search criteria is provided
        has_query = query and query.strip()
        has_filters = any([expertise_id, field_id, area_id, level_id])
        
        if not has_query and not has_filters:
            raise HTTPException(
                status_code=400, 
                detail="At least one search criteria must be provided (query or filters)"
            )
        
        # Use None for empty query to ensure repository filtering works correctly
        search_name = query.strip() if (query and query.strip()) else None
        
        offset = (page - 1) * page_size
        candidates = candidate_repo.search_candidates_with_filters(
            name=search_name,
            expertise_id=expertise_id,
            field_id=field_id,
            area_id=area_id,
            level_id=level_id,
            limit=page_size,
            offset=offset
        )

        total = candidate_repo.count_candidates_with_filters(
            name=search_name,
            expertise_id=expertise_id,
            field_id=field_id,
            area_id=area_id,
            level_id=level_id,
        )

        candidate_responses = [entity_to_response_model(candidate, CandidateResponse) for candidate in candidates]
        
        if candidate_responses:
            expertise_ids = {c.expertise_id for c in candidates}
            field_ids = {c.field_id for c in candidates}
            area_ids = {c.area_id for c in candidates}
            level_ids = {c.level_id for c in candidates}
            headhunter_ids = {c.headhunter_id for c in candidates}

            expertises = expertise_repo.get_expertises_by_ids(list(expertise_ids))
            fields = field_repo.get_fields_by_ids(list(field_ids))
            areas = area_repo.get_areas_by_ids(list(area_ids))
            levels = level_repo.get_levels_by_ids(list(level_ids))
            headhunters = headhunter_repo.get_headhunters_by_ids(list(headhunter_ids))

            expertise_map = {e.expertise_id: e.name for e in expertises}
            field_map = {f.field_id: f.name for f in fields}
            area_map = {a.area_id: a.name for a in areas}
            level_map = {l.level_id: l.name for l in levels}
            headhunter_map = {h.headhunter_id: h.name for h in headhunters}

            for candidate_response in candidate_responses:
                candidate_response.expertise_name = expertise_map.get(candidate_response.expertise_id)
                candidate_response.field_name = field_map.get(candidate_response.field_id)
                candidate_response.area_name = area_map.get(candidate_response.area_id)
                candidate_response.level_name = level_map.get(candidate_response.level_id)
                candidate_response.headhunter_name = headhunter_map.get(candidate_response.headhunter_id)
        
        search_description = []
        if search_name:
            search_description.append(f"query '{search_name}'")
        if any([expertise_id, field_id, area_id, level_id]):
            search_description.append("filters")
        
        message = f"Found {total} candidates matching {' and '.join(search_description)}"
        
        return create_list_response(
            data=candidate_responses,
            total=total,
            page=page,
            page_size=page_size,
            message=message
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