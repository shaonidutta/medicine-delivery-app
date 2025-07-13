"""
Medicine model
"""

from sqlalchemy import String, DateTime, func, ForeignKey, Boolean, Numeric, Integer, Date, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, date
from typing import Optional, List, Dict, Any
from app.database.base import Base, uuid_pk


class Medicine(Base):
    __tablename__ = "medicines"

    id: Mapped[uuid_pk]
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    generic_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    manufacturer: Mapped[str] = mapped_column(String(255), nullable=False)
    category_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("categories.id"), nullable=True, index=True)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    dosage_form: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    strength: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    prescription_required: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, index=True)
    stock_quantity: Mapped[int] = mapped_column(Integer, default=0, nullable=False, index=True)
    min_stock_level: Mapped[int] = mapped_column(Integer, default=10, nullable=False)
    expiry_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    batch_number: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    storage_conditions: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    side_effects: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)
    contraindications: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)
    active_ingredients: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    category: Mapped[Optional["Category"]] = relationship("Category")

    def __repr__(self) -> str:
        return f"<Medicine(id={self.id}, name={self.name}, manufacturer={self.manufacturer})>"
