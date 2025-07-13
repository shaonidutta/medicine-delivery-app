"""
Category model
"""

from sqlalchemy import String, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import Optional, List
from app.database.base import Base, uuid_pk


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[uuid_pk]
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    parent_category_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("categories.id"), nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships (simplified for now)
    # parent_category: Mapped[Optional["Category"]] = relationship("Category", remote_side="Category.id")
    # subcategories: Mapped[List["Category"]] = relationship("Category")

    def __repr__(self) -> str:
        return f"<Category(id={self.id}, name={self.name})>"
