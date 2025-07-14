"""
Order and OrderItem models
"""

from sqlalchemy import String, DateTime, func, ForeignKey, Numeric, Integer, Boolean, JSON, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import Optional, Dict, Any
from app.database.base import Base, uuid_pk


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[uuid_pk]
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(50), default="pending", nullable=False, index=True)  # pending, confirmed, preparing, out_for_delivery, delivered, cancelled
    total_amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    delivery_address: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)
    delivery_partner_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("delivery_partners.id", ondelete="SET NULL"), nullable=True, index=True)
    pharmacy_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("pharmacies.id", ondelete="SET NULL"), nullable=True)
    estimated_delivery_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    actual_delivery_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    emergency_order: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    delivery_proof_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    cancellation_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user: Mapped["User"] = relationship("User")
    delivery_partner: Mapped[Optional["DeliveryPartner"]] = relationship("DeliveryPartner")
    pharmacy: Mapped[Optional["Pharmacy"]] = relationship("Pharmacy")
    items: Mapped[list["OrderItem"]] = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Order(id={self.id}, user_id={self.user_id}, status={self.status}, total_amount={self.total_amount})>"


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[uuid_pk]
    order_id: Mapped[str] = mapped_column(String, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, index=True)
    medicine_id: Mapped[str] = mapped_column(String, ForeignKey("medicines.id", ondelete="CASCADE"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    total_price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    prescription_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("prescriptions.id", ondelete="SET NULL"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    order: Mapped["Order"] = relationship("Order", back_populates="items")
    medicine: Mapped["Medicine"] = relationship("Medicine")
    prescription: Mapped[Optional["Prescription"]] = relationship("Prescription")

    def __repr__(self) -> str:
        return f"<OrderItem(id={self.id}, order_id={self.order_id}, medicine_id={self.medicine_id}, quantity={self.quantity})>"
