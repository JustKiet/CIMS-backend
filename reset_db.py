# reset_db.py

from app.database.session import PostgresSessionFactory
from app.database.models import Base
from app.config import settings

def main():
    # Fill in with your actual DB credentials or load from config
    host = "localhost"
    port = settings.POSTGRES_PORT
    name = settings.POSTGRES_DB
    user = settings.POSTGRES_USER
    password = settings.POSTGRES_PASSWORD

    factory = PostgresSessionFactory(host, port, name, user, password)
    engine = factory._engine # type: ignore

    print("Dropping all tables...")
    Base.metadata.drop_all(engine)
    print("All tables dropped!")

    print("Re-creating all tables...")
    Base.metadata.create_all(engine)
    print("All tables created!")

if __name__ == "__main__":
    main()