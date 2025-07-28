from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import date, datetime
from cims.core.repositories.project_repository import ProjectRepository
from cims.core.entities.project import Project
from cims.core.exceptions import NotFoundError
from cims.deps import get_project_repository
from cims.schemas import (
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse,
    ProjectDetailResponse,
    ProjectListResponse,
    ErrorResponse,
)
from cims.schemas.utils import create_list_response, entity_to_response_model

router = APIRouter(
    prefix="/projects",
    tags=["projects"],
    responses={
        404: {"model": ErrorResponse, "description": "Project not found"},
        400: {"model": ErrorResponse, "description": "Invalid request data"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    }
)

@router.post("/",
    response_model=ProjectDetailResponse,
    status_code=201,
    summary="Create a new project",
    description="Create a new project in the system"
)
async def create_project(
    project_data: ProjectCreate,
    project_repo: ProjectRepository = Depends(get_project_repository),
):
    """Create a new project."""
    try:
        project = Project(
            project_id=None,
            name=project_data.name,
            start_date=project_data.start_date or date.today(),
            end_date=project_data.end_date or date.today(),
            budget=project_data.budget or 0.0,
            budget_currency="USD",  # Default currency
            type="CODINH",  # Default project type
            required_recruits=1,  # Default required recruits
            recruited=0,  # Default recruited count
            status="TIMKIEMUNGVIEN",  # Default status
            customer_id=project_data.customer_id,
            expertise_id=1,  # Default expertise_id, should be passed from client
            area_id=1,  # Default area_id, should be passed from client
            level_id=1,  # Default level_id, should be passed from client
            created_at=None,
            updated_at=None
        )
        
        created_project = project_repo.create_project(project)
        project_response = entity_to_response_model(created_project, ProjectResponse)
        
        return ProjectDetailResponse(
            success=True,
            message="Project created successfully",
            data=project_response
        )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/",
    response_model=ProjectListResponse,
    summary="Get all projects",
    description="Retrieve a paginated list of all projects"
)
async def get_projects(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Number of items per page"),
    project_repo: ProjectRepository = Depends(get_project_repository)
):
    """Get all projects with pagination."""
    try:
        offset = (page - 1) * page_size
        projects = project_repo.get_all_projects(limit=page_size, offset=offset)
        
        project_responses = [entity_to_response_model(project, ProjectResponse) for project in projects]
        total = len(projects)
        
        return create_list_response(
            data=project_responses,
            total=total,
            page=page,
            page_size=page_size,
            message="Projects retrieved successfully"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search",
    response_model=ProjectListResponse,
    summary="Search projects",
    description="Search projects by name with pagination"
)
async def search_projects(
    query: str = Query(..., min_length=1, description="Search query"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Number of items per page"),
    project_repo: ProjectRepository = Depends(get_project_repository)
):
    """Search projects by name."""
    try:
        offset = (page - 1) * page_size
        projects = project_repo.search_projects_by_name(
            name_query=query,
            limit=page_size,
            offset=offset
        )
        
        project_responses = [entity_to_response_model(project, ProjectResponse) for project in projects]
        total = len(projects)
        
        return create_list_response(
            data=project_responses,
            total=total,
            page=page,
            page_size=page_size,
            message=f"Found {total} projects matching '{query}'"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{project_id}",
    response_model=ProjectDetailResponse,
    summary="Get project by ID",
    description="Retrieve a specific project by its ID"
)
async def get_project(
    project_id: int,
    project_repo: ProjectRepository = Depends(get_project_repository)
):
    """Get a project by ID."""
    try:
        project = project_repo.get_project_by_id(project_id)
        
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        project_response = entity_to_response_model(project, ProjectResponse)
        
        return ProjectDetailResponse(
            success=True,
            message="Project retrieved successfully",
            data=project_response
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{project_id}",
    response_model=ProjectDetailResponse,
    summary="Update project",
    description="Update an existing project's information"
)
async def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    project_repo: ProjectRepository = Depends(get_project_repository),
):
    """Update a project."""
    try:
        existing_project = project_repo.get_project_by_id(project_id)
        
        if not existing_project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        update_data = project_data.model_dump(exclude_unset=True)
        
        # Create updated project entity with existing values and new updates
        updated_project_entity = Project(
            project_id=existing_project.project_id,
            name=update_data.get('name', existing_project.name),
            start_date=update_data.get('start_date', existing_project.start_date),
            end_date=update_data.get('end_date', existing_project.end_date),
            budget=update_data.get('budget', existing_project.budget),
            budget_currency=existing_project.budget_currency,
            type=existing_project.type,
            required_recruits=existing_project.required_recruits,
            recruited=existing_project.recruited,
            status=update_data.get('status', existing_project.status),
            customer_id=update_data.get('customer_id', existing_project.customer_id),
            expertise_id=existing_project.expertise_id,
            area_id=existing_project.area_id,
            level_id=existing_project.level_id,
            created_at=existing_project.created_at,
            updated_at=datetime.now()
        )
        
        updated_project = project_repo.update_project(updated_project_entity)
        project_response = entity_to_response_model(updated_project, ProjectResponse)
        
        return ProjectDetailResponse(
            success=True,
            message="Project updated successfully",
            data=project_response
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{project_id}",
    status_code=204,
    summary="Delete project",
    description="Delete a project from the system"
)
async def delete_project(
    project_id: int,
    project_repo: ProjectRepository = Depends(get_project_repository)
):
    """Delete a project."""
    try:
        project_repo.delete_project(project_id)
        return None  # 204 No Content
        
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Project not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
