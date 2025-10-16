from fastapi import APIRouter, Depends, HTTPException, Query
import datetime
from cims.core.repositories.field_repository import FieldRepository
from cims.core.entities.field import Field
from cims.core.exceptions import NotFoundError
from cims.deps import get_field_repository
from cims.schemas import (
    FieldCreate,
    FieldUpdate,
    FieldResponse,
    FieldDetailResponse,
    FieldListResponse,
    ErrorResponse,
)
from cims.schemas.utils import create_list_response, entity_to_response_model

router = APIRouter(
    prefix="/fields",
    tags=["fields"],
    responses={
        404: {"model": ErrorResponse, "description": "Field not found"},
        400: {"model": ErrorResponse, "description": "Invalid request data"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    }
)

@router.post("/",
    response_model=FieldDetailResponse,
    status_code=201,
    summary="Create a new field",
    description="Create a new field in the system"
)
async def create_field(
    field_data: FieldCreate,
    field_repo: FieldRepository = Depends(get_field_repository),
):
    """Create a new field."""
    try:
        field = Field(
            field_id=None,
            name=field_data.name
        )
        
        created_field = field_repo.create_field(field)
        field_response = entity_to_response_model(created_field, FieldResponse)
        
        return FieldDetailResponse(
            success=True,
            message="Field created successfully",
            data=field_response
        )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/",
    response_model=FieldListResponse,
    summary="Get all fields",
    description="Retrieve a paginated list of all fields"
)
async def get_fields(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Number of items per page"),
    field_repo: FieldRepository = Depends(get_field_repository)
):
    """Get all fields with pagination."""
    try:
        offset = (page - 1) * page_size
        fields = field_repo.get_all_fields(limit=page_size, offset=offset)
        
        field_responses = [entity_to_response_model(field, FieldResponse) for field in fields]
        total = len(fields)
        
        return create_list_response(
            data=field_responses,
            total=total,
            page=page,
            page_size=page_size,
            message="Fields retrieved successfully"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search",
    response_model=FieldListResponse,
    summary="Search fields",
    description="Search fields by name with pagination"
)
async def search_fields(
    query: str = Query(..., min_length=1, description="Search query"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Number of items per page"),
    field_repo: FieldRepository = Depends(get_field_repository)
):
    """Search fields by name."""
    try:
        offset = (page - 1) * page_size
        fields = field_repo.search_fields_by_name(
            name_query=query,
            limit=page_size,
            offset=offset
        )
        
        field_responses = [entity_to_response_model(field, FieldResponse) for field in fields]
        total = len(fields)
        
        return create_list_response(
            data=field_responses,
            total=total,
            page=page,
            page_size=page_size,
            message=f"Found {total} fields matching '{query}'"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{field_id}",
    response_model=FieldDetailResponse,
    summary="Get field by ID",
    description="Retrieve a specific field by its ID"
)
async def get_field(
    field_id: int,
    field_repo: FieldRepository = Depends(get_field_repository)
):
    """Get a field by ID."""
    try:
        field = field_repo.get_field_by_id(field_id)
        
        if not field:
            raise HTTPException(status_code=404, detail="Field not found")
        
        field_response = entity_to_response_model(field, FieldResponse)
        
        return FieldDetailResponse(
            success=True,
            message="Field retrieved successfully",
            data=field_response
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{field_id}",
    response_model=FieldDetailResponse,
    summary="Update field",
    description="Update an existing field's information"
)
async def update_field(
    field_id: int,
    field_data: FieldUpdate,
    field_repo: FieldRepository = Depends(get_field_repository),
):
    """Update a field."""
    try:
        existing_field = field_repo.get_field_by_id(field_id)
        
        if not existing_field:
            raise HTTPException(status_code=404, detail="Field not found")
        
        update_data = field_data.model_dump(exclude_unset=True)
        
        # Create updated field entity with existing values and new updates
        updated_field_entity = Field(
            field_id=existing_field.field_id,
            name=update_data.get('name', existing_field.name),
            created_at=existing_field.created_at,
            updated_at=datetime.datetime.now(datetime.timezone.utc)
        )
        
        updated_field = field_repo.update_field(updated_field_entity)
        field_response = entity_to_response_model(updated_field, FieldResponse)
        
        return FieldDetailResponse(
            success=True,
            message="Field updated successfully",
            data=field_response
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{field_id}",
    status_code=204,
    summary="Delete field",
    description="Delete a field from the system"
)
async def delete_field(
    field_id: int,
    field_repo: FieldRepository = Depends(get_field_repository)
):
    """Delete a field."""
    try:
        field_repo.delete_field(field_id)
        return None  # 204 No Content
        
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Field not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
