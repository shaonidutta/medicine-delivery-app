"""
Cart Pydantic schemas
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from decimal import Decimal


class CartItemBase(BaseModel):
    medicine_id: str = Field(..., description="Medicine ID")
    quantity: int = Field(..., ge=1, le=100, description="Quantity of medicine")
    prescription_id: Optional[str] = Field(None, description="Prescription ID if required")
    notes: Optional[str] = Field(None, max_length=500, description="Special instructions")


class CartItemCreate(CartItemBase):
    pass


class CartItemUpdate(BaseModel):
    quantity: Optional[int] = Field(None, ge=1, le=100, description="New quantity")
    prescription_id: Optional[str] = Field(None, description="Prescription ID if required")
    notes: Optional[str] = Field(None, max_length=500, description="Special instructions")


class CartItemResponse(CartItemBase):
    id: str
    cart_id: str
    unit_price: float
    total_price: float
    medicine: Optional[Dict[str, Any]] = None
    prescription: Optional[Dict[str, Any]] = None
    is_prescription_valid: bool = True
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class CartBase(BaseModel):
    pass


class CartResponse(CartBase):
    id: str
    user_id: str
    items: List[CartItemResponse] = []
    total_items: int = 0
    subtotal: float = 0.0
    tax_amount: float = 0.0
    delivery_fee: float = 0.0
    total_amount: float = 0.0
    has_prescription_items: bool = False
    prescription_validation_status: str = "valid"  # valid, invalid, pending
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class AddToCartRequest(BaseModel):
    medicine_id: str = Field(..., description="Medicine ID to add")
    quantity: int = Field(1, ge=1, le=100, description="Quantity to add")
    prescription_id: Optional[str] = Field(None, description="Prescription ID if medicine requires prescription")
    notes: Optional[str] = Field(None, max_length=500, description="Special instructions")

    @validator('quantity')
    @classmethod
    def validate_quantity(cls, v):
        if v <= 0:
            raise ValueError('Quantity must be greater than 0')
        if v > 100:
            raise ValueError('Quantity cannot exceed 100')
        return v


class UpdateCartItemRequest(BaseModel):
    quantity: int = Field(..., ge=1, le=100, description="New quantity")
    prescription_id: Optional[str] = Field(None, description="Prescription ID if required")
    notes: Optional[str] = Field(None, max_length=500, description="Special instructions")


class CartSummary(BaseModel):
    total_items: int
    subtotal: float
    tax_amount: float
    delivery_fee: float
    total_amount: float
    has_prescription_items: bool
    prescription_validation_status: str


class CartValidationResult(BaseModel):
    is_valid: bool
    errors: List[str] = []
    warnings: List[str] = []
    prescription_issues: List[Dict[str, Any]] = []


class CartCheckoutRequest(BaseModel):
    delivery_address: Dict[str, Any] = Field(..., description="Delivery address details")
    payment_method: str = Field(..., description="Payment method")
    delivery_instructions: Optional[str] = Field(None, max_length=500, description="Special delivery instructions")
    use_prescription_validation: bool = Field(True, description="Whether to validate prescriptions before checkout")


class BulkCartOperation(BaseModel):
    items: List[AddToCartRequest] = Field(..., description="List of items to add to cart")
    clear_existing: bool = Field(False, description="Whether to clear existing cart items first")


class CartItemAvailability(BaseModel):
    medicine_id: str
    available_quantity: int
    is_in_stock: bool
    requires_prescription: bool
    prescription_valid: bool = True
    estimated_delivery: Optional[str] = None
