from cims.database.session import PostgresSessionFactory
from cims.auth import Authenticator
from cims.config import settings
from fastapi import Depends
from sqlalchemy.orm import Session
from contextlib import contextmanager

# Repository interfaces
from cims.core.repositories.headhunter_repository import HeadhunterRepository
from cims.core.repositories.candidate_repository import CandidateRepository
from cims.core.repositories.project_repository import ProjectRepository
from cims.core.repositories.customer_repository import CustomerRepository
from cims.core.repositories.area_repository import AreaRepository
from cims.core.repositories.level_repository import LevelRepository
from cims.core.repositories.expertise_repository import ExpertiseRepository
from cims.core.repositories.field_repository import FieldRepository
from cims.core.repositories.nominee_repository import NomineeRepository

# SQLAlchemy implementations
from cims.clients.sqlalchemy.headhunter_repository import SQLAlchemyHeadhunterRepository
from cims.clients.sqlalchemy.candidate_repository import SQLAlchemyCandidateRepository
from cims.clients.sqlalchemy.project_repository import SQLAlchemyProjectRepository
from cims.clients.sqlalchemy.customer_repository import SQLAlchemyCustomerRepository
from cims.clients.sqlalchemy.area_repository import SQLAlchemyAreaRepository
from cims.clients.sqlalchemy.level_repository import SQLAlchemyLevelRepository
from cims.clients.sqlalchemy.expertise_repository import SQLAlchemyExpertiseRepository
from cims.clients.sqlalchemy.field_repository import SQLAlchemyFieldRepository
from cims.clients.sqlalchemy.nominee_repository import SQLAlchemyNomineeRepository

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

def get_headhunter_repository(db_session: Session = Depends(get_db_session)) -> HeadhunterRepository:
    return SQLAlchemyHeadhunterRepository(db_session)

def get_candidate_repository(db_session: Session = Depends(get_db_session)) -> CandidateRepository:
    return SQLAlchemyCandidateRepository(db_session)

def get_project_repository(db_session: Session = Depends(get_db_session)) -> ProjectRepository:
    return SQLAlchemyProjectRepository(db_session)

def get_customer_repository(db_session: Session = Depends(get_db_session)) -> CustomerRepository:
    return SQLAlchemyCustomerRepository(db_session)

def get_area_repository(db_session: Session = Depends(get_db_session)) -> AreaRepository:
    return SQLAlchemyAreaRepository(db_session)

def get_level_repository(db_session: Session = Depends(get_db_session)) -> LevelRepository:
    return SQLAlchemyLevelRepository(db_session)

def get_expertise_repository(db_session: Session = Depends(get_db_session)) -> ExpertiseRepository:
    return SQLAlchemyExpertiseRepository(db_session)

def get_field_repository(db_session: Session = Depends(get_db_session)) -> FieldRepository:
    return SQLAlchemyFieldRepository(db_session)

def get_nominee_repository(db_session: Session = Depends(get_db_session)) -> NomineeRepository:
    return SQLAlchemyNomineeRepository(db_session)

def get_authenticator(headhunter_repository: HeadhunterRepository = Depends(get_headhunter_repository)) -> Authenticator:
    return Authenticator(
        secret_key=settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
        access_token_expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        headhunter_repository=headhunter_repository
    )

# Utility functions for creating repositories outside of FastAPI DI
def create_headhunter_repository() -> HeadhunterRepository:
    session = create_db_session()
    return SQLAlchemyHeadhunterRepository(session)

def create_candidate_repository() -> CandidateRepository:
    session = create_db_session()
    return SQLAlchemyCandidateRepository(session)

def create_project_repository() -> ProjectRepository:
    session = create_db_session()
    return SQLAlchemyProjectRepository(session)

def create_customer_repository() -> CustomerRepository:
    session = create_db_session()
    return SQLAlchemyCustomerRepository(session)

def create_area_repository() -> AreaRepository:
    session = create_db_session()
    return SQLAlchemyAreaRepository(session)

def create_level_repository() -> LevelRepository:
    session = create_db_session()
    return SQLAlchemyLevelRepository(session)

def create_expertise_repository() -> ExpertiseRepository:
    session = create_db_session()
    return SQLAlchemyExpertiseRepository(session)

def create_field_repository() -> FieldRepository:
    session = create_db_session()
    return SQLAlchemyFieldRepository(session)

def create_nominee_repository() -> NomineeRepository:
    session = create_db_session()
    return SQLAlchemyNomineeRepository(session)

@contextmanager
def get_repositories():
    """
    Context manager that provides all repositories with a shared session.
    Ensures the session is properly closed when done.
    """
    session = create_db_session()
    try:
        yield {
            'candidate': SQLAlchemyCandidateRepository(session),
            'expertise': SQLAlchemyExpertiseRepository(session),
            'field': SQLAlchemyFieldRepository(session),
            'area': SQLAlchemyAreaRepository(session),
            'level': SQLAlchemyLevelRepository(session),
            'headhunter': SQLAlchemyHeadhunterRepository(session),
            'project': SQLAlchemyProjectRepository(session),
            'customer': SQLAlchemyCustomerRepository(session),
            'nominee': SQLAlchemyNomineeRepository(session),
        }
    finally:
        session.close()