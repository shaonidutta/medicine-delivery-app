"""
User model
"""

from sqlalchemy import Boolean, String, Date, JSON, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date, datetime
from typing import Optional, List, Dict, Any
from app.database.base import Base, uuid_pk


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid_pk]
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    phone: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    date_of_birth: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    medical_conditions: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)
    allergies: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)
    emergency_contact: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    delivery_addresses: Mapped[Optional[List[Dict[str, Any]]]] = mapped_column(JSON, nullable=True)
    phone_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email}, name={self.first_name} {self.last_name})>"
