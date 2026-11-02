
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

load_dotenv()

# Database URL from .env file
SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")

if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("SQLALCHEMY_DATABASE_URL is missing from .env file")

# Create database engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create database session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Create declarative base
Base = declarative_base()


# Database dependency for FastAPI
def get_db():
    db: Session = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# Create database tables
def create_table():
    Base.metadata.create_all(bind=engine)