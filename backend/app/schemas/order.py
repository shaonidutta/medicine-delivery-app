"""
Order Pydantic schemas
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from enum import Enum


class OrderStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
    PACKED = "packed"
    SHIPPED = "shipped"
    OUT_FOR_DELIVERY = "out_for_delivery"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    RETURNED = "returned"


class PaymentStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"


class PaymentMethod(str, Enum):
    CASH_ON_DELIVERY = "cash_on_delivery"
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    UPI = "upi"
    NET_BANKING = "net_banking"
    WALLET = "wallet"


class DeliveryAddress(BaseModel):
    street: str = Field(..., min_length=1, max_length=255)
    city: str = Field(..., min_length=1, max_length=100)
    state: str = Field(..., min_length=1, max_length=100)
    postal_code: str = Field(..., min_length=1, max_length=20)
    country: str = Field(default="India", max_length=100)
    landmark: Optional[str] = Field(None, max_length=255)
    contact_phone: str = Field(..., min_length=10, max_length=15)
    contact_name: str = Field(..., min_length=1, max_length=100)


class OrderItemBase(BaseModel):
    medicine_id: str = Field(..., description="Medicine ID")
    quantity: int = Field(..., ge=1, le=100, description="Quantity ordered")
    unit_price: float = Field(..., gt=0, description="Price per unit at time of order")
    prescription_id: Optional[str] = Field(None, description="Prescription ID if required")


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemResponse(OrderItemBase):
    id: str
    order_id: str
    total_price: float
    medicine: Optional[Dict[str, Any]] = None
    prescription: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    delivery_address: DeliveryAddress = Field(..., description="Delivery address")
    payment_method: PaymentMethod = Field(..., description="Payment method")
    delivery_instructions: Optional[str] = Field(None, max_length=500, description="Special delivery instructions")
    expected_delivery_date: Optional[date] = None


class OrderCreate(OrderBase):
    items: List[OrderItemCreate] = Field(..., min_items=1, description="Order items")


class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None
    payment_status: Optional[PaymentStatus] = None
    delivery_partner_id: Optional[str] = None
    tracking_number: Optional[str] = None
    delivery_instructions: Optional[str] = Field(None, max_length=500)
    expected_delivery_date: Optional[date] = None
    actual_delivery_date: Optional[date] = None


class OrderResponse(OrderBase):
    id: str
    user_id: str
    order_number: str
    status: OrderStatus
    payment_status: PaymentStatus
    items: List[OrderItemResponse] = []
    subtotal: float
    tax_amount: float
    delivery_fee: float
    total_amount: float
    tracking_number: Optional[str] = None
    delivery_partner_id: Optional[str] = None
    pharmacy_id: Optional[str] = None
    estimated_delivery_time: Optional[int] = None  # in minutes
    actual_delivery_date: Optional[date] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class OrderSearchQuery(BaseModel):
    status: Optional[OrderStatus] = Field(None, description="Filter by order status")
    payment_status: Optional[PaymentStatus] = Field(None, description="Filter by payment status")
    date_from: Optional[date] = Field(None, description="Filter orders from this date")
    date_to: Optional[date] = Field(None, description="Filter orders until this date")
    delivery_partner_id: Optional[str] = Field(None, description="Filter by delivery partner")
    pharmacy_id: Optional[str] = Field(None, description="Filter by pharmacy")
    page: int = Field(1, ge=1, description="Page number")
    page_size: int = Field(20, ge=1, le=100, description="Items per page")


class OrderSearchResponse(BaseModel):
    orders: List[OrderResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class OrderStatusUpdate(BaseModel):
    status: OrderStatus = Field(..., description="New order status")
    notes: Optional[str] = Field(None, max_length=500, description="Status update notes")
    estimated_delivery_time: Optional[int] = Field(None, ge=1, description="Estimated delivery time in minutes")


class OrderTrackingInfo(BaseModel):
    order_id: str
    order_number: str
    status: OrderStatus
    tracking_number: Optional[str] = None
    delivery_partner: Optional[str] = None
    estimated_delivery_time: Optional[int] = None
    status_history: List[Dict[str, Any]] = []
    current_location: Optional[str] = None
    delivery_address: DeliveryAddress


class OrderStats(BaseModel):
    total_orders: int
    pending_orders: int
    confirmed_orders: int
    processing_orders: int
    delivered_orders: int
    cancelled_orders: int
    total_revenue: float
    average_order_value: float


class CreateOrderFromCart(BaseModel):
    delivery_address: DeliveryAddress = Field(..., description="Delivery address")
    payment_method: PaymentMethod = Field(..., description="Payment method")
    delivery_instructions: Optional[str] = Field(None, max_length=500, description="Special delivery instructions")
    validate_prescriptions: bool = Field(True, description="Whether to validate prescriptions before creating order")


class OrderCancellation(BaseModel):
    reason: str = Field(..., min_length=1, max_length=500, description="Reason for cancellation")
    refund_requested: bool = Field(False, description="Whether refund is requested")


class OrderDeliveryUpdate(BaseModel):
    delivery_partner_id: str = Field(..., description="Delivery partner ID")
    estimated_delivery_time: int = Field(..., ge=1, le=180, description="Estimated delivery time in minutes")
    tracking_number: Optional[str] = Field(None, description="Tracking number")
    pickup_time: Optional[datetime] = Field(None, description="Pickup time from pharmacy")
