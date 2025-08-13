"""
Test Configuration for CIMS Backend
"""
import sys
import os
from pathlib import Path
from typing import Generator
import tempfile

# Add the backend directory to Python path so we can import the app module
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# Import after adding to path
from cims.database.models import Base
from cims.deps import get_db_session

# Create a test app without the lifespan events
from cims.api.v1.auth import router as auth_router
from cims.api.v1.candidate import router as candidate_router
from cims.api.v1.headhunter import router as headhunter_router
from cims.api.v1.project import router as project_router
from cims.api.v1.customer import router as customer_router
from cims.api.v1.area import router as area_router
from cims.api.v1.level import router as level_router
from cims.api.v1.expertise import router as expertise_router
from cims.api.v1.field import router as field_router
from cims.api.v1.nominee import router as nominee_router

# Test settings
TEST_SECRET_KEY: str = "test-secret-key"
TEST_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

# Create a temporary database file for each test session
@pytest.fixture(scope="session")
def temp_db() -> Generator[str, None, None]:
    """Create a temporary database file."""
    db_fd, db_path = tempfile.mkstemp()
    yield f"sqlite:///{db_path}"
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture(scope="session")
def db_engine(temp_db: str):
    """Create test database engine."""
    engine = create_engine(temp_db, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

from sqlalchemy.engine import Engine

@pytest.fixture(scope="function")
def db_session(db_engine: Engine) -> Generator[Session, None, None]:
    """Create a fresh database session for each test."""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
    connection = db_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def test_app():
    """Create a test FastAPI app without lifespan events."""
    app = FastAPI(title="CIMS Test API")
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(auth_router, prefix="/api/v1", tags=["Authentication"])
    app.include_router(candidate_router, prefix="/api/v1", tags=["Candidates"])
    app.include_router(headhunter_router, prefix="/api/v1", tags=["Headhunters"])
    app.include_router(project_router, prefix="/api/v1", tags=["Projects"])
    app.include_router(customer_router, prefix="/api/v1", tags=["Customers"])
    app.include_router(area_router, prefix="/api/v1", tags=["Areas"])
    app.include_router(level_router, prefix="/api/v1", tags=["Levels"])
    app.include_router(expertise_router, prefix="/api/v1", tags=["Expertise"])
    app.include_router(field_router, prefix="/api/v1", tags=["Fields"])
    app.include_router(nominee_router, prefix="/api/v1", tags=["Nominees"])
    
    return app

@pytest.fixture(scope="function")
def client(test_app: FastAPI, db_session: Session) -> Generator[TestClient, None, None]:
    """Create a test client with dependency override."""
    def override_get_db() -> Generator[Session, None, None]:
        try:
            yield db_session
        finally:
            pass
    
    test_app.dependency_overrides[get_db_session] = override_get_db
    with TestClient(test_app) as test_client:
        yield test_client
    test_app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def setup_test_data(client: TestClient) -> dict:
    """Set up basic test data that many tests depend on."""
    test_data = {}
    
    # Create a field first (required by customers)
    field_data = {
        "name": "Test Field",
        "description": "A test field for testing"
    }
    field_response = client.post("/api/v1/fields/", json=field_data)
    if field_response.status_code == 201:
        test_data["field"] = field_response.json()["data"]
    
    # Create a customer (required by projects)
    customer_data = {
        "name": "Test Customer",
        "field_id": test_data["field"]["field_id"] if "field" in test_data else 1,
        "representative_name": "John Doe",
        "representative_phone": "1234567890",
        "representative_email": "john@testcustomer.com",
        "representative_role": "Manager"
    }
    customer_response = client.post("/api/v1/customers/", json=customer_data)
    if customer_response.status_code == 201:
        test_data["customer"] = customer_response.json()["data"]
    
    # Create an expertise (required by projects)
    expertise_data = {
        "name": "Test Expertise",
        "description": "A test expertise for testing"
    }
    expertise_response = client.post("/api/v1/expertises/", json=expertise_data)
    if expertise_response.status_code == 201:
        test_data["expertise"] = expertise_response.json()["data"]
    
    # Create an area (required by projects)
    area_data = {
        "name": "Test Area",
        "description": "A test area for testing"
    }
    area_response = client.post("/api/v1/areas/", json=area_data)
    if area_response.status_code == 201:
        test_data["area"] = area_response.json()["data"]
    
    # Create a level (required by projects)
    level_data = {
        "name": "Test Level",
        "description": "A test level for testing"
    }
    level_response = client.post("/api/v1/levels/", json=level_data)
    if level_response.status_code == 201:
        test_data["level"] = level_response.json()["data"]
    
    return test_data
