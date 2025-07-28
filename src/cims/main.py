from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
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
from cims.config import CLogger, settings
from cims.database.session import PostgresSessionFactory

logger = CLogger(__name__).get_logger()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting CIMS API...")
    logger.info("Creating database tables...")
    factory = PostgresSessionFactory(
        host=settings.POSTGRES_HOST,
        port=settings.POSTGRES_PORT,
        name=settings.POSTGRES_DB,
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD
    )
    factory.create_tables()
    logger.info("Database tables created successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down CIMS API...")

app = FastAPI(lifespan=lifespan)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to the CIMS API"}

@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify if the API is running.
    """
    return {"status": "ok"}

# Include the authentication router
app.include_router(auth_router, prefix="/api/v1", tags=["auth"])

# Include all CRUD API routers
app.include_router(candidate_router, prefix="/api/v1")
app.include_router(headhunter_router, prefix="/api/v1")
app.include_router(project_router, prefix="/api/v1")
app.include_router(customer_router, prefix="/api/v1")
app.include_router(area_router, prefix="/api/v1")
app.include_router(level_router, prefix="/api/v1")
app.include_router(expertise_router, prefix="/api/v1")
app.include_router(field_router, prefix="/api/v1")
app.include_router(nominee_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)