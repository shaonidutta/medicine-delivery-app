"""
Database session configuration
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings

# Create engine with proper configuration for different databases
database_url = str(settings.DATABASE_URL)

# Configure engine based on database type
if "sqlite" in database_url:
    engine = create_engine(
        database_url,
        echo=True if not settings.TESTING else False,
        connect_args={"check_same_thread": False},
    )
elif "postgresql" in database_url:
    engine = create_engine(
        database_url,
        echo=True if not settings.TESTING else False,
        pool_pre_ping=True,
        pool_recycle=300,
    )
else:
    # Default configuration
    engine = create_engine(
        database_url,
        echo=True if not settings.TESTING else False,
    )

# Create session factory
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)


def get_db() -> Session:
    """
    Dependency to get database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
