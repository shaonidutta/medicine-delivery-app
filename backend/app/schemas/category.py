"""
Category Pydantic schemas
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    parent_category_id: Optional[str] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    parent_category_id: Optional[str] = None


class CategoryResponse(CategoryBase):
    id: str
    created_at: datetime
    updated_at: datetime
    subcategories: Optional[List["CategoryResponse"]] = None

    class Config:
        orm_mode = True


class CategoryWithMedicineCount(CategoryResponse):
    medicine_count: int = 0


# Update forward references
CategoryResponse.model_rebuild()
