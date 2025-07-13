"""
Database session configuration
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings

# Create engine
engine = create_engine(
    str(settings.DATABASE_URL),
    echo=True if not settings.TESTING else False,
    connect_args={"check_same_thread": False} if "sqlite" in str(settings.DATABASE_URL) else {},
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
