from cims.core.services.field_service import FieldService
from fastapi import APIRouter, Depends, HTTPException, Query
import datetime
from cims.core.services.customer_service import CustomerService
from cims.core.entities.customer import Customer
from cims.core.exceptions import NotFoundError
from cims.deps import get_customer_service, get_field_service
from cims.schemas import (
    CustomerCreate,
    CustomerUpdate,
    CustomerResponse,
    CustomerDetailResponse,
    CustomerListResponse,
    ErrorResponse,
)
from cims.schemas.utils import create_list_response, entity_to_response_model

router = APIRouter(
    prefix="/customers",
    tags=["customers"],
    responses={
        404: {"model": ErrorResponse, "description": "Customer not found"},
        400: {"model": ErrorResponse, "description": "Invalid request data"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    }
)

@router.post("/",
    response_model=CustomerDetailResponse,
    status_code=201,
    summary="Create a new customer",
    description="Create a new customer in the system"
)
async def create_customer(
    customer_data: CustomerCreate,
    customer_repo: CustomerService = Depends(get_customer_service),
):
    """Create a new customer."""
    try:
        customer = Customer(
            customer_id=None,
            name=customer_data.name,
            field_id=customer_data.field_id,
            representative_name=customer_data.representative_name,
            representative_phone=customer_data.representative_phone,
            representative_email=str(customer_data.representative_email),
            representative_role=customer_data.representative_role,
            created_at=None,
            updated_at=None
        )
        
        created_customer = customer_repo.create_customer(customer)
        customer_response = entity_to_response_model(created_customer, CustomerResponse)
        
        return CustomerDetailResponse(
            success=True,
            message="Customer created successfully",
            data=customer_response
        )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/",
    response_model=CustomerListResponse,
    summary="Get all customers",
    description="Retrieve a paginated list of all customers"
)
async def get_customers(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Number of items per page"),
    customer_repo: CustomerService = Depends(get_customer_service),
    field_repo: FieldService = Depends(get_field_service)
):
    """Get all customers with pagination."""
    try:
        offset = (page - 1) * page_size
        customers = customer_repo.get_all_customers(limit=page_size, offset=offset)
        
        customer_responses = [entity_to_response_model(customer, CustomerResponse) for customer in customers]

        if customer_responses:
            field_ids = {c.field_id for c in customers}
            fields = field_repo.get_fields_by_ids(list(field_ids))
            field_map = {f.field_id: f.name for f in fields}

            for customer_response in customer_responses:
                customer_response.field_name = field_map.get(customer_response.field_id)

        total = len(customers)
        
        return create_list_response(
            data=customer_responses,
            total=total,
            page=page,
            page_size=page_size,
            message="Customers retrieved successfully"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search",
    response_model=CustomerListResponse,
    summary="Search customers",
    description="Search customers by name, email, company, or phone with pagination"
)
async def search_customers(
    query: str = Query(..., min_length=1, description="Search query"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Number of items per page"),
    customer_repo: CustomerService = Depends(get_customer_service),
    field_repo: FieldService = Depends(get_field_service)
):
    """Search customers by name, email, company, or phone."""
    try:
        offset = (page - 1) * page_size
        customers = customer_repo.search_customers_by_name(
            name_query=query,
            limit=page_size,
            offset=offset
        )
        
        customer_responses = [entity_to_response_model(customer, CustomerResponse) for customer in customers]

        if customer_responses:
            field_ids = {c.field_id for c in customers}
            fields = field_repo.get_fields_by_ids(list(field_ids))
            field_map = {f.field_id: f.name for f in fields}

            for customer_response in customer_responses:
                customer_response.field_name = field_map.get(customer_response.field_id)

        total = len(customers)
        
        return create_list_response(
            data=customer_responses,
            total=total,
            page=page,
            page_size=page_size,
            message=f"Found {total} customers matching '{query}'"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{customer_id}",
    response_model=CustomerDetailResponse,
    summary="Get customer by ID",
    description="Retrieve a specific customer by their ID"
)
async def get_customer(
    customer_id: int,
    customer_repo: CustomerService = Depends(get_customer_service),
    field_repo: FieldService = Depends(get_field_service)
):
    """Get a customer by ID."""
    try:
        customer = customer_repo.get_customer_by_id(customer_id)
        
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        
        customer_response = entity_to_response_model(customer, CustomerResponse)

        # Fetch field name if available
        field = field_repo.get_field_by_id(customer.field_id)
        if field:
            customer_response.field_name = field.name
        
        return CustomerDetailResponse(
            success=True,
            message="Customer retrieved successfully",
            data=customer_response
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{customer_id}",
    response_model=CustomerDetailResponse,
    summary="Update customer",
    description="Update an existing customer's information"
)
async def update_customer(
    customer_id: int,
    customer_data: CustomerUpdate,
    customer_repo: CustomerService = Depends(get_customer_service),
):
    """Update a customer."""
    try:
        existing_customer = customer_repo.get_customer_by_id(customer_id)
        
        if not existing_customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        
        update_data = customer_data.model_dump(exclude_unset=True)
        
        # Create a new entity with updated data
        updated_customer = Customer(
            customer_id=existing_customer.customer_id,
            name=update_data.get('name', existing_customer.name),
            field_id=update_data.get('field_id', existing_customer.field_id),
            representative_name=update_data.get('representative_name', existing_customer.representative_name),
            representative_phone=update_data.get('representative_phone', existing_customer.representative_phone),
            representative_email=str(update_data.get('representative_email', existing_customer.representative_email)),
            representative_role=update_data.get('representative_role', existing_customer.representative_role),
            created_at=existing_customer.created_at,
            updated_at=datetime.datetime.now(datetime.timezone.utc)
        )
        
        saved_customer = customer_repo.update_customer(updated_customer)
        customer_response = entity_to_response_model(saved_customer, CustomerResponse)
        
        return CustomerDetailResponse(
            success=True,
            message="Customer updated successfully",
            data=customer_response
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{customer_id}",
    status_code=204,
    summary="Delete customer",
    description="Delete a customer from the system"
)
async def delete_customer(
    customer_id: int,
    customer_repo: CustomerService = Depends(get_customer_service)
):
    """Delete a customer."""
    try:
        customer_repo.delete_customer(customer_id)
        return None  # 204 No Content
        
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Customer not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))