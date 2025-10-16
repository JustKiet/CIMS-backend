from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import date, datetime
from cims.core.repositories.project_repository import ProjectRepository
from cims.core.repositories.customer_repository import CustomerRepository
from cims.core.repositories.expertise_repository import ExpertiseRepository
from cims.core.repositories.area_repository import AreaRepository
from cims.core.repositories.level_repository import LevelRepository
from cims.core.entities.project import Project
from cims.core.exceptions import NotFoundError
from cims.deps import (
    get_project_repository,
    get_customer_repository,
    get_expertise_repository,
    get_area_repository,
    get_level_repository
)
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
    customer_repo: CustomerRepository = Depends(get_customer_repository),
    expertise_repo: ExpertiseRepository = Depends(get_expertise_repository),
):
    """Create a new project."""
    try:
        customer_name = customer_repo.get_customer_by_id(project_data.customer_id)

        if not customer_name:
            raise HTTPException(status_code=404, detail="Customer not found")
        
        expertise_name = expertise_repo.get_expertise_by_id(project_data.expertise_id)

        if not expertise_name:
            raise HTTPException(status_code=404, detail="Expertise not found")
        
        project_name = f"[{customer_name.name}] {expertise_name.name}"
        
        project = Project(
            project_id=None,
            name=project_name,
            start_date=project_data.start_date,
            end_date=project_data.end_date,
            budget=project_data.budget,
            budget_currency=project_data.budget_currency,
            type=project_data.type,
            required_recruits=project_data.required_recruits,
            recruited=project_data.recruited,
            status=project_data.status,
            customer_id=project_data.customer_id,
            expertise_id=project_data.expertise_id,
            area_id=project_data.area_id,
            level_id=project_data.level_id,
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
    project_repo: ProjectRepository = Depends(get_project_repository),
    customer_repo: CustomerRepository = Depends(get_customer_repository),
    expertise_repo: ExpertiseRepository = Depends(get_expertise_repository),
    area_repo: AreaRepository = Depends(get_area_repository),
    level_repo: LevelRepository = Depends(get_level_repository)
):
    """Get all projects with pagination."""
    try:
        offset = (page - 1) * page_size
        projects = project_repo.get_all_projects(limit=page_size, offset=offset)
        total = project_repo.count_all_projects()
        
        project_responses = [entity_to_response_model(project, ProjectResponse) for project in projects]

        if project_responses:
            # Step 1: Collect all unique IDs
            customer_ids = {p.customer_id for p in project_responses}
            expertise_ids = {p.expertise_id for p in project_responses}
            area_ids = {p.area_id for p in project_responses}
            level_ids = {p.level_id for p in project_responses}

            # Step 2: Fetch all needed data in bulk
            customers = customer_repo.get_customers_by_ids(list(customer_ids))
            expertises = expertise_repo.get_expertises_by_ids(list(expertise_ids))
            areas = area_repo.get_areas_by_ids(list(area_ids))
            levels = level_repo.get_levels_by_ids(list(level_ids))

            # Step 3: Build lookup dictionaries
            customer_map = {c.customer_id: c.name for c in customers}
            expertise_map = {e.expertise_id: e.name for e in expertises}
            area_map = {a.area_id: a.name for a in areas}
            level_map = {l.level_id: l.name for l in levels}

            # Step 4: Map names onto project_responses
            for project_response in project_responses:
                project_response.customer_name = customer_map[project_response.customer_id]
                project_response.expertise_name = expertise_map[project_response.expertise_id]
                project_response.area_name = area_map[project_response.area_id]
                project_response.level_name = level_map[project_response.level_id]

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
    description="Search projects by name, customer, or expertise with pagination"
)
async def search_projects(
    query: str = Query(..., min_length=1, description="Search query"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Number of items per page"),
    project_repo: ProjectRepository = Depends(get_project_repository),
    customer_repo: CustomerRepository = Depends(get_customer_repository),
    expertise_repo: ExpertiseRepository = Depends(get_expertise_repository),
    area_repo: AreaRepository = Depends(get_area_repository),
    level_repo: LevelRepository = Depends(get_level_repository)
):
    """Search projects by name, customer name, or expertise name."""
    try:
        offset = (page - 1) * page_size
        projects = project_repo.search_projects_comprehensive(
            query=query,
            limit=page_size,
            offset=offset
        )
        total = project_repo.count_projects_comprehensive(query)
        
        project_responses = [entity_to_response_model(project, ProjectResponse) for project in projects]
        
        if project_responses:
            # Step 1: Collect all unique IDs
            customer_ids = {p.customer_id for p in project_responses}
            expertise_ids = {p.expertise_id for p in project_responses}
            area_ids = {p.area_id for p in project_responses}
            level_ids = {p.level_id for p in project_responses}

            # Step 2: Fetch all needed data in bulk
            customers = customer_repo.get_customers_by_ids(list(customer_ids))
            expertises = expertise_repo.get_expertises_by_ids(list(expertise_ids))
            areas = area_repo.get_areas_by_ids(list(area_ids))
            levels = level_repo.get_levels_by_ids(list(level_ids))

            # Step 3: Build lookup dictionaries
            customer_map = {c.customer_id: c.name for c in customers}
            expertise_map = {e.expertise_id: e.name for e in expertises}
            area_map = {a.area_id: a.name for a in areas}
            level_map = {l.level_id: l.name for l in levels}

            # Step 4: Map names onto project_responses
            for project_response in project_responses:
                project_response.customer_name = customer_map[project_response.customer_id]
                project_response.expertise_name = expertise_map[project_response.expertise_id]
                project_response.area_name = area_map[project_response.area_id]
                project_response.level_name = level_map[project_response.level_id]

        return create_list_response(
            data=project_responses,
            total=total,
            page=page,
            page_size=page_size,
            message=f"Found {total} projects matching '{query}'"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/customer/{customer_id}",
    response_model=ProjectListResponse,
    summary="Get projects by customer ID",
    description="Retrieve all projects for a specific customer with pagination"
)
async def get_projects_by_customer(
    customer_id: int,
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Number of items per page"),
    project_repo: ProjectRepository = Depends(get_project_repository),
    customer_repo: CustomerRepository = Depends(get_customer_repository),
    expertise_repo: ExpertiseRepository = Depends(get_expertise_repository),
    area_repo: AreaRepository = Depends(get_area_repository),
    level_repo: LevelRepository = Depends(get_level_repository)
):
    """Get all projects for a specific customer with pagination."""
    try:
        # Verify customer exists
        customer = customer_repo.get_customer_by_id(customer_id)
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        
        offset = (page - 1) * page_size
        projects = project_repo.get_projects_by_customer_id(
            customer_id=customer_id,
            limit=page_size,
            offset=offset
        )
        total = project_repo.count_projects_by_customer_id(customer_id)
        
        project_responses = [entity_to_response_model(project, ProjectResponse) for project in projects]

        if project_responses:
            # Step 1: Collect all unique IDs
            customer_ids = {p.customer_id for p in project_responses}
            expertise_ids = {p.expertise_id for p in project_responses}
            area_ids = {p.area_id for p in project_responses}
            level_ids = {p.level_id for p in project_responses}

            # Step 2: Fetch all needed data in bulk
            customers = customer_repo.get_customers_by_ids(list(customer_ids))
            expertises = expertise_repo.get_expertises_by_ids(list(expertise_ids))
            areas = area_repo.get_areas_by_ids(list(area_ids))
            levels = level_repo.get_levels_by_ids(list(level_ids))

            # Step 3: Build lookup dictionaries
            customer_map = {c.customer_id: c.name for c in customers}
            expertise_map = {e.expertise_id: e.name for e in expertises}
            area_map = {a.area_id: a.name for a in areas}
            level_map = {l.level_id: l.name for l in levels}

            # Step 4: Map names onto project_responses
            for project_response in project_responses:
                project_response.customer_name = customer_map[project_response.customer_id]
                project_response.expertise_name = expertise_map[project_response.expertise_id]
                project_response.area_name = area_map[project_response.area_id]
                project_response.level_name = level_map[project_response.level_id]

        return create_list_response(
            data=project_responses,
            total=total,
            page=page,
            page_size=page_size,
            message=f"Found {total} projects for customer"
        )
        
    except HTTPException:
        raise
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
            budget_currency=update_data.get('budget_currency', existing_project.budget_currency),
            type=update_data.get('type', existing_project.type),
            required_recruits=update_data.get('required_recruits', existing_project.required_recruits),
            recruited=update_data.get('recruited', existing_project.recruited),
            status=update_data.get('status', existing_project.status),
            customer_id=update_data.get('customer_id', existing_project.customer_id),
            expertise_id=update_data.get('expertise_id', existing_project.expertise_id),
            area_id=update_data.get('area_id', existing_project.area_id),
            level_id=update_data.get('level_id', existing_project.level_id),
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
