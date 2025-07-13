"""
Delivery Partner, Pharmacy, and PharmacyMedicine models
"""

from sqlalchemy import String, DateTime, func, ForeignKey, Boolean, Numeric, Integer, JSON, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import Optional, Dict, Any
from app.database.base import Base, uuid_pk


class DeliveryPartner(Base):
    __tablename__ = "delivery_partners"

    id: Mapped[uuid_pk]
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    vehicle_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # bike, scooter, car
    license_number: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    current_location: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)  # {lat, lng}
    is_available: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, index=True)
    rating: Mapped[float] = mapped_column(Numeric(3, 2), default=0.00, nullable=False)
    total_deliveries: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self) -> str:
        return f"<DeliveryPartner(id={self.id}, name={self.name}, is_available={self.is_available})>"


class Pharmacy(Base):
    __tablename__ = "pharmacies"

    id: Mapped[uuid_pk]
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    address: Mapped[str] = mapped_column(String, nullable=False)
    location: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)  # {lat, lng}
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    license_number: Mapped[str] = mapped_column(String(100), nullable=False)
    operating_hours: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    medicines: Mapped[list["PharmacyMedicine"]] = relationship("PharmacyMedicine", back_populates="pharmacy")

    def __repr__(self) -> str:
        return f"<Pharmacy(id={self.id}, name={self.name}, is_active={self.is_active})>"


class PharmacyMedicine(Base):
    __tablename__ = "pharmacy_medicines"
    __table_args__ = (UniqueConstraint('pharmacy_id', 'medicine_id', name='_pharmacy_medicine_uc'),)

    id: Mapped[uuid_pk]
    pharmacy_id: Mapped[str] = mapped_column(String, ForeignKey("pharmacies.id", ondelete="CASCADE"), nullable=False, index=True)
    medicine_id: Mapped[str] = mapped_column(String, ForeignKey("medicines.id", ondelete="CASCADE"), nullable=False, index=True)
    stock_quantity: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    price: Mapped[Optional[float]] = mapped_column(Numeric(10, 2), nullable=True)
    last_updated: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    pharmacy: Mapped["Pharmacy"] = relationship("Pharmacy", back_populates="medicines")
    medicine: Mapped["Medicine"] = relationship("Medicine")

    def __repr__(self) -> str:
        return f"<PharmacyMedicine(pharmacy_id={self.pharmacy_id}, medicine_id={self.medicine_id}, stock={self.stock_quantity})>"
