from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine

class PostgresSessionFactory:
    def __init__(
        self,
        host: str,
        port: int,
        name: str,
        user: str,
        password: str
    ) -> None:
        self._database_url = f"postgresql://{user}:{password}@{host}:{port}/{name}"
        self._engine = create_engine(self._database_url, pool_pre_ping=True, pool_size=10, max_overflow=20)
        self._Session = sessionmaker(bind=self._engine, autoflush=False, autocommit=False)

    def create_tables(self) -> None:
        """
        Create all tables in the database.
        This method should be called once to initialize the database schema.
        """
        from app.infrastructure.database.models import Base
        Base.metadata.create_all(self._engine)

    def get_session(self) -> Session:
        return self._Session()
    
