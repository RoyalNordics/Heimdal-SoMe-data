import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check if we're in testing mode
TESTING = os.getenv("TESTING", "false").lower() == "true"

# Get the absolute path to the project directory
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Database connection settings
if TESTING:
    # Use SQLite for testing
    DB_FILE = os.path.join(PROJECT_DIR, "test.db")
    DATABASE_URL = f"sqlite:///{DB_FILE}"
    engine = create_engine(
        DATABASE_URL, connect_args={"check_same_thread": False}
    )
    print(f"Using SQLite database for testing: {DB_FILE}")
else:
    # Use PostgreSQL for production
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "heimdal_some_data")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

    # Create the database URL
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    # Create the SQLAlchemy engine
    try:
        engine = create_engine(DATABASE_URL)
        print(f"Using PostgreSQL database at {DB_HOST}:{DB_PORT}/{DB_NAME}")
    except Exception as e:
        print(f"Error connecting to PostgreSQL: {e}")
        print("Falling back to SQLite database")
        DATABASE_URL = "sqlite:///./heimdal_data.db"
        engine = create_engine(
            DATABASE_URL, connect_args={"check_same_thread": False}
        )

# Create a SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

def get_db():
    """
    Get a database session.
    
    Yields:
        Session: A SQLAlchemy session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    Initialize the database by creating all tables.
    """
    from .models import Base
    Base.metadata.create_all(bind=engine)

def check_db_connection():
    """
    Check if the database connection is working.
    
    Returns:
        bool: True if the connection is working, False otherwise.
    """
    try:
        # Try to connect to the database
        connection = engine.connect()
        connection.close()
        return True
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return False
