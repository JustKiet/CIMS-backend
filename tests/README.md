# CIMS Backend Tests

This directory contains comprehensive tests for the CIMS (Customer Information Management System) backend API.

## Test Structure

```
tests/
├── conftest.py              # Test configuration and fixtures
├── requirements-test.txt    # Test dependencies
├── functional/              # End-to-end API tests
│   ├── test_area_api.py     # Area endpoints testing
│   ├── test_customer_api.py # Customer endpoints testing
│   ├── test_project_api.py  # Project endpoints testing
│   └── test_auth_api.py     # Authentication endpoints testing
└── unit/                    # Unit tests
    └── test_schemas.py      # Schema validation tests
```

## Running Tests

### Prerequisites

1. Install test dependencies:
```bash
pip install -r tests/requirements-test.txt
```

2. Ensure the main application dependencies are installed:
```bash
pip install -r requirements.in
```

3. **Important**: Make sure you're in the virtual environment and in the backend directory:
```bash
# Activate virtual environment (if not already activated)
source .venv/bin/activate

# Ensure you're in the backend directory
cd /path/to/cims/backend
```

### Running All Tests

```bash
# From the backend directory (with virtual environment activated)
pytest tests/

# With coverage report
pytest tests/ --cov=app --cov-report=html
```

### Running Specific Test Categories

```bash
# Functional tests only
pytest tests/functional/

# Unit tests only
pytest tests/unit/

# Specific test file
pytest tests/functional/test_area_api.py

# Specific test method
pytest tests/functional/test_area_api.py::TestAreaAPI::test_create_area_success
```

## Test Configuration

The test suite is configured to use SQLite for testing, avoiding dependencies on external PostgreSQL instances. Key configuration features:

- **Isolated Database**: Each test session uses a temporary SQLite database
- **Dependency Injection**: Database sessions are properly mocked using pytest fixtures
- **Clean Slate**: Each test gets a fresh database session with proper transaction rollback
- **No External Dependencies**: Tests run without requiring Docker or external services

## Test Categories

### Functional Tests

These tests validate the entire API endpoints from request to response:

- **Area API Tests** (`test_area_api.py`):
  - CRUD operations for areas
  - Pagination and search functionality
  - Data validation and error handling

- **Customer API Tests** (`test_customer_api.py`):
  - Customer creation with contact information
  - Email and phone validation
  - Customer search and retrieval

- **Project API Tests** (`test_project_api.py`):
  - Project lifecycle management
  - Date range validation
  - Budget and status tracking

- **Authentication API Tests** (`test_auth_api.py`):
  - Headhunter registration and validation
  - Login/logout functionality
  - Token-based authentication
  - User profile retrieval

### Unit Tests

These tests focus on individual components:

- **Schema Tests** (`test_schemas.py`):
  - Pydantic model validation
  - Field constraints and types
  - Schema utility functions
  - Update model behavior

## Test Data

All tests use isolated test data and do not affect the production database. Each test creates and cleans up its own data using temporary SQLite databases.

## API Validation Coverage

The tests cover:

✅ **Request Validation**
- Required field validation
- Data type validation
- Format validation (email, phone, dates)
- Length constraints

✅ **Response Validation**
- Correct HTTP status codes
- Response schema compliance
- Pagination metadata
- Error message format

✅ **Business Logic**
- CRUD operations
- Search functionality
- Data relationships
- Edge cases

## Test Configuration Details

The `conftest.py` file contains:

- **Path Setup**: Automatically adds the backend directory to Python path
- **Test App Creation**: Creates a FastAPI app instance without production lifespan events
- **Database Fixtures**: Sets up temporary SQLite databases with proper cleanup
- **Dependency Overrides**: Replaces production database connections with test connections
- **Session Management**: Handles database transactions and rollbacks

### Key Fixtures

- `temp_db`: Creates a temporary SQLite database file
- `db_engine`: Sets up the SQLAlchemy engine with test database
- `db_session`: Provides a fresh database session for each test
- `test_app`: Creates a test FastAPI application
- `client`: Provides a TestClient with dependency overrides

## Extending Tests

To add new tests:

1. **For new endpoints**: Create functional tests in `tests/functional/`
2. **For new schemas**: Add validation tests in `tests/unit/test_schemas.py`
3. **For new entities**: Create corresponding test files following the naming pattern
4. **Use fixtures**: Always use the `client` fixture in functional tests for proper database isolation

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure you're running tests from the backend directory with the virtual environment activated
2. **Database Errors**: The tests use SQLite, so no external database setup is required
3. **Module Not Found**: Ensure the `app/__init__.py` file exists to make the app directory a Python package

### Debug Mode

Run tests with verbose output and no capture to see detailed information:
```bash
pytest tests/ -v -s
```

## Continuous Integration

These tests are designed to run in CI/CD pipelines and provide:
- Fast feedback on code changes
- Regression prevention
- API contract validation
- Documentation through examples

## Performance Considerations

- Tests use lightweight SQLite for speed
- Minimal test data creation
- Parallel execution support
- Cleanup after each test
- Temporary database files are automatically removed

## Common Test Patterns

```python
# Standard test structure
class TestEntityAPI:
    def test_create_entity_success(self, client: TestClient) -> None:
        # Setup
        entity_data = {...}
        
        # Action
        response = client.post("/api/v1/entities/", json=entity_data)
        
        # Assertions
        assert response.status_code == 201
        assert response.json()["success"] is True
        
    def test_create_entity_validation_error(self, client: TestClient) -> None:
        # Test with invalid data
        invalid_data = {...}
        response = client.post("/api/v1/entities/", json=invalid_data)
        assert response.status_code == 422
```
