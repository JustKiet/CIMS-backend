from app.database.session import PostgresSessionFactory
from app.auth import Authenticator
from app.config import settings
from fastapi import Depends
from sqlalchemy.orm import Session

# Repository interfaces
from app.core.repositories.headhunter_repository import HeadhunterRepository
from app.core.repositories.candidate_repository import CandidateRepository
from app.core.repositories.project_repository import ProjectRepository
from app.core.repositories.customer_repository import CustomerRepository
from app.core.repositories.area_repository import AreaRepository
from app.core.repositories.level_repository import LevelRepository
from app.core.repositories.expertise_repository import ExpertiseRepository
from app.core.repositories.field_repository import FieldRepository
from app.core.repositories.nominee_repository import NomineeRepository

# SQLAlchemy implementations
from app.clients.sqlalchemy.headhunter_repository import SQLAlchemyHeadhunterRepository
from app.clients.sqlalchemy.candidate_repository import SQLAlchemyCandidateRepository
from app.clients.sqlalchemy.project_repository import SQLAlchemyProjectRepository
from app.clients.sqlalchemy.customer_repository import SQLAlchemyCustomerRepository
from app.clients.sqlalchemy.area_repository import SQLAlchemyAreaRepository
from app.clients.sqlalchemy.level_repository import SQLAlchemyLevelRepository
from app.clients.sqlalchemy.expertise_repository import SQLAlchemyExpertiseRepository
from app.clients.sqlalchemy.field_repository import SQLAlchemyFieldRepository
from app.clients.sqlalchemy.nominee_repository import SQLAlchemyNomineeRepository

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