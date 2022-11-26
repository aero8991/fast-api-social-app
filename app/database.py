from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL
from . config import settings

#SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
url = URL.create("postgresql", username=settings.database_username,
                 password=settings.database_password, host=settings.database_hostname, database=settings.database_name)
SQLALCHEMY_DATABASE_URL = url

engine = create_engine(
    SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
