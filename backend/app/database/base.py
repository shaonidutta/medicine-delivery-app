"""
Database base configuration
"""

from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase
import uuid
from sqlalchemy import String
from sqlalchemy.orm import mapped_column
from typing import Annotated

# Custom UUID type for PostgreSQL
uuid_pk = Annotated[uuid.UUID, mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))]

class Base(DeclarativeBase):
    """Base class for all database models"""
    pass

# Create metadata instance
metadata = MetaData()

# Note: Model imports will be handled in alembic env.py to avoid circular imports
