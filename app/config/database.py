from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# SQLite Database Configuration
# Database file will be created in the project root
SQLALCHEMY_DATABASE_URL = "sqlite:///./internship_portal.db"

# Create the SQLAlchemy engine
# check_same_thread=False is needed for SQLite to work with multiple threads
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a SessionLocal class
# Each instance of SessionLocal will be a new database session.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class
# We will inherit from this class to create each of the database models (ORM models).
Base = declarative_base()

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
