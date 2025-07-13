"""
Prescription model
"""

from sqlalchemy import String, DateTime, func, ForeignKey, Date, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, date
from typing import Optional, Dict, Any
from app.database.base import Base, uuid_pk


class Prescription(Base):
    __tablename__ = "prescriptions"

    id: Mapped[uuid_pk]
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    image_url: Mapped[str] = mapped_column(String(500), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="pending", nullable=False, index=True)  # pending, verified, rejected
    doctor_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    doctor_license: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    issue_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    expiry_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    extracted_medicines: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    verification_notes: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    verified_by: Mapped[Optional[str]] = mapped_column(String, ForeignKey("users.id"), nullable=True, index=True)
    verified_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user: Mapped["User"] = relationship("User", foreign_keys=[user_id])
    verified_by_user: Mapped[Optional["User"]] = relationship("User", foreign_keys=[verified_by])

    def __repr__(self) -> str:
        return f"<Prescription(id={self.id}, user_id={self.user_id}, status={self.status})>"
