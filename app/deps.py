from app.infrastructure.database.session import PostgresSessionFactory
from app.infrastructure.auth import Authenticator
from app.infrastructure.config import settings
from fastapi import Depends
from sqlalchemy.orm import Session
from app.domain.repositories.headhunter_repository import HeadhunterRepository
from app.infrastructure.gateways.sqlalchemy_headhunter_repository import SQLAlchemyHeadhunterRepository

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

def get_headhunter_repository(session: Session = Depends(get_db_session)) -> HeadhunterRepository:
    return SQLAlchemyHeadhunterRepository(session)

def get_authenticator(headhunter_repository: HeadhunterRepository = Depends(get_headhunter_repository)) -> Authenticator:
    return Authenticator(
        secret_key=settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
        access_token_expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        headhunter_repository=headhunter_repository
    )

PostgresSessionFactory(
    host=settings.POSTGRES_HOST,
    port=settings.POSTGRES_PORT,
    name=settings.POSTGRES_DB,
    user=settings.POSTGRES_USER,
    password=settings.POSTGRES_PASSWORD
).create_tables()