"""
Cart and CartItem models
"""

from sqlalchemy import String, DateTime, func, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import Optional
from app.database.base import Base, uuid_pk


class Cart(Base):
    __tablename__ = "carts"

    id: Mapped[uuid_pk]
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user: Mapped["User"] = relationship("User")
    items: Mapped[list["CartItem"]] = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Cart(id={self.id}, user_id={self.user_id})>"


class CartItem(Base):
    __tablename__ = "cart_items"
    __table_args__ = (UniqueConstraint('cart_id', 'medicine_id', name='_cart_medicine_uc'),)

    id: Mapped[uuid_pk]
    cart_id: Mapped[str] = mapped_column(String, ForeignKey("carts.id", ondelete="CASCADE"), nullable=False, index=True)
    medicine_id: Mapped[str] = mapped_column(String, ForeignKey("medicines.id", ondelete="CASCADE"), nullable=False, index=True)
    quantity: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    prescription_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("prescriptions.id", ondelete="SET NULL"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    cart: Mapped["Cart"] = relationship("Cart", back_populates="items")
    medicine: Mapped["Medicine"] = relationship("Medicine")
    # prescription: Mapped[Optional["Prescription"]] = relationship("Prescription")

    def __repr__(self) -> str:
        return f"<CartItem(id={self.id}, cart_id={self.cart_id}, medicine_id={self.medicine_id}, quantity={self.quantity})>"
