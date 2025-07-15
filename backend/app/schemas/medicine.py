"""
Medicine Pydantic schemas
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from decimal import Decimal


class MedicineBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    generic_name: Optional[str] = Field(None, max_length=255)
    manufacturer: str = Field(..., min_length=1, max_length=255)
    category_id: Optional[str] = None
    description: Optional[str] = None
    dosage_form: Optional[str] = Field(None, max_length=100)
    strength: Optional[str] = Field(None, max_length=100)
    price: float = Field(..., gt=0)
    prescription_required: bool = False
    stock_quantity: int = Field(default=0, ge=0)
    min_stock_level: int = Field(default=10, ge=0)
    expiry_date: Optional[date] = None
    batch_number: Optional[str] = Field(None, max_length=100)
    storage_conditions: Optional[str] = None
    side_effects: Optional[List[str]] = None
    contraindications: Optional[List[str]] = None
    active_ingredients: Optional[Dict[str, Any]] = None

    @validator('expiry_date')
    @classmethod
    def validate_expiry_date(cls, v):
        if v and v <= date.today():
            raise ValueError('Expiry date must be in the future')
        return v


class MedicineCreate(MedicineBase):
    pass


class MedicineUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    generic_name: Optional[str] = Field(None, max_length=255)
    manufacturer: Optional[str] = Field(None, min_length=1, max_length=255)
    category_id: Optional[str] = None
    description: Optional[str] = None
    dosage_form: Optional[str] = Field(None, max_length=100)
    strength: Optional[str] = Field(None, max_length=100)
    price: Optional[float] = Field(None, gt=0)
    prescription_required: Optional[bool] = None
    stock_quantity: Optional[int] = Field(None, ge=0)
    min_stock_level: Optional[int] = Field(None, ge=0)
    expiry_date: Optional[date] = None
    batch_number: Optional[str] = Field(None, max_length=100)
    storage_conditions: Optional[str] = None
    side_effects: Optional[List[str]] = None
    contraindications: Optional[List[str]] = None
    active_ingredients: Optional[Dict[str, Any]] = None

    @validator('expiry_date')
    @classmethod
    def validate_expiry_date(cls, v):
        if v and v <= date.today():
            raise ValueError('Expiry date must be in the future')
        return v


class MedicineResponse(MedicineBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class MedicineSearchQuery(BaseModel):
    q: Optional[str] = Field(None, description="Search query for medicine name or generic name")
    category_id: Optional[str] = Field(None, description="Filter by category ID")
    prescription_required: Optional[bool] = Field(None, description="Filter by prescription requirement")
    min_price: Optional[float] = Field(None, ge=0, description="Minimum price filter")
    max_price: Optional[float] = Field(None, ge=0, description="Maximum price filter")
    in_stock: Optional[bool] = Field(None, description="Filter medicines in stock")
    manufacturer: Optional[str] = Field(None, description="Filter by manufacturer")
    dosage_form: Optional[str] = Field(None, description="Filter by dosage form")
    sort_by: Optional[str] = Field("name", description="Sort by: name, price, created_at")
    sort_order: Optional[str] = Field("asc", description="Sort order: asc, desc")
    page: int = Field(1, ge=1, description="Page number")
    page_size: int = Field(20, ge=1, le=100, description="Items per page")


class MedicineSearchResponse(BaseModel):
    medicines: List[MedicineResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class MedicineAlternatives(BaseModel):
    medicine_id: str
    alternatives: List[MedicineResponse]
