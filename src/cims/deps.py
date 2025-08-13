from cims.database.session import PostgresSessionFactory
from cims.auth import Authenticator
from cims.config import settings
from fastapi import Depends
from sqlalchemy.orm import Session
from contextlib import contextmanager

# Service interfaces
from cims.core.services.headhunter_service import HeadhunterService
from cims.core.services.candidate_service import CandidateService
from cims.core.services.project_service import ProjectService
from cims.core.services.customer_service import CustomerService
from cims.core.services.area_service import AreaService
from cims.core.services.level_service import LevelService
from cims.core.services.expertise_service import ExpertiseService
from cims.core.services.field_service import FieldService
from cims.core.services.nominee_service import NomineeService

# SQLAlchemy implementations
from cims.services.sqlalchemy import (
    SQLAlchemyHeadhunterService,
    SQLAlchemyCandidateService,
    SQLAlchemyProjectService,
    SQLAlchemyCustomerService,
    SQLAlchemyAreaService,
    SQLAlchemyLevelService,
    SQLAlchemyExpertiseService,
    SQLAlchemyFieldService,
    SQLAlchemyNomineeService
)

def get_db_session(): 
    factory = PostgresSessionFactory(
        host=settings.POSTGRES_HOST,
        port=settings.POSTGRES_PORT,
        name=settings.POSTGRES_DB,
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD
    )

    session = factory.get_session()
    try:
        yield session
    finally:
        session.close()

def create_db_session() -> Session:
    """
    Create a database session for use outside of FastAPI dependency injection.
    Remember to close the session when done.
    """
    factory = PostgresSessionFactory(
        host=settings.POSTGRES_HOST,
        port=settings.POSTGRES_PORT,
        name=settings.POSTGRES_DB,
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD
    )
    return factory.get_session()

def get_headhunter_service(db_session: Session = Depends(get_db_session)) -> HeadhunterService:
    return SQLAlchemyHeadhunterService(db_session)

def get_candidate_service(db_session: Session = Depends(get_db_session)) -> CandidateService:
    return SQLAlchemyCandidateService(db_session)

def get_project_service(db_session: Session = Depends(get_db_session)) -> ProjectService:
    return SQLAlchemyProjectService(db_session)

def get_customer_service(db_session: Session = Depends(get_db_session)) -> CustomerService:
    return SQLAlchemyCustomerService(db_session)

def get_area_service(db_session: Session = Depends(get_db_session)) -> AreaService:
    return SQLAlchemyAreaService(db_session)

def get_level_service(db_session: Session = Depends(get_db_session)) -> LevelService:
    return SQLAlchemyLevelService(db_session)

def get_expertise_service(db_session: Session = Depends(get_db_session)) -> ExpertiseService:
    return SQLAlchemyExpertiseService(db_session)

def get_field_service(db_session: Session = Depends(get_db_session)) -> FieldService:
    return SQLAlchemyFieldService(db_session)

def get_nominee_service(db_session: Session = Depends(get_db_session)) -> NomineeService:
    return SQLAlchemyNomineeService(db_session)

def get_authenticator(headhunter_service: HeadhunterService = Depends(get_headhunter_service)) -> Authenticator:
    return Authenticator(
        secret_key=settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
        access_token_expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        headhunter_service=headhunter_service
    )

# Utility functions for creating repositories outside of FastAPI DI
def create_headhunter_service() -> HeadhunterService:
    session = create_db_session()
    return SQLAlchemyHeadhunterService(session)

def create_candidate_service() -> CandidateService:
    session = create_db_session()
    return SQLAlchemyCandidateService(session)

def create_project_service() -> ProjectService:
    session = create_db_session()
    return SQLAlchemyProjectService(session)

def create_customer_service() -> CustomerService:
    session = create_db_session()
    return SQLAlchemyCustomerService(session)

def create_area_service() -> AreaService:
    session = create_db_session()
    return SQLAlchemyAreaService(session)

def create_level_service() -> LevelService:
    session = create_db_session()
    return SQLAlchemyLevelService(session)

def create_expertise_service() -> ExpertiseService:
    session = create_db_session()
    return SQLAlchemyExpertiseService(session)

def create_field_service() -> FieldService:
    session = create_db_session()
    return SQLAlchemyFieldService(session)

def create_nominee_service() -> NomineeService:
    session = create_db_session()
    return SQLAlchemyNomineeService(session)

@contextmanager
def get_repositories():
    """
    Context manager that provides all repositories with a shared session.
    Ensures the session is properly closed when done.
    """
    session = create_db_session()
    try:
        yield {
            'candidate': SQLAlchemyCandidateService(session),
            'expertise': SQLAlchemyExpertiseService(session),
            'field': SQLAlchemyFieldService(session),
            'area': SQLAlchemyAreaService(session),
            'level': SQLAlchemyLevelService(session),
            'headhunter': SQLAlchemyHeadhunterService(session),
            'project': SQLAlchemyProjectService(session),
            'customer': SQLAlchemyCustomerService(session),
            'nominee': SQLAlchemyNomineeService(session),
        }
    finally:
        session.close()