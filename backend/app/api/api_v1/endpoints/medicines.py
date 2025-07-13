"""
Medicine management endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, and_, func
from typing import List, Optional
import math
from app.database.session import get_db
from app.models.medicine import Medicine
from app.models.category import Category
from app.schemas.medicine import (
    MedicineCreate, MedicineUpdate, MedicineResponse, 
    MedicineSearchQuery, MedicineSearchResponse, MedicineAlternatives
)
from app.api.api_v1.endpoints.auth import get_current_user
from app.models.user import User

router = APIRouter()


@router.get("/search", response_model=MedicineSearchResponse)
def search_medicines(
    q: Optional[str] = Query(None, description="Search query for medicine name or generic name"),
    category_id: Optional[str] = Query(None, description="Filter by category ID"),
    prescription_required: Optional[bool] = Query(None, description="Filter by prescription requirement"),
    min_price: Optional[float] = Query(None, ge=0, description="Minimum price filter"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price filter"),
    in_stock: Optional[bool] = Query(None, description="Filter medicines in stock"),
    manufacturer: Optional[str] = Query(None, description="Filter by manufacturer"),
    dosage_form: Optional[str] = Query(None, description="Filter by dosage form"),
    sort_by: str = Query("name", description="Sort by: name, price, created_at"),
    sort_order: str = Query("asc", description="Sort order: asc, desc"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
) -> MedicineSearchResponse:
    """
    Search medicines with advanced filtering and pagination
    """
    # Build query
    query = db.query(Medicine).options(joinedload(Medicine.category))
    
    # Apply filters
    if q:
        search_filter = or_(
            Medicine.name.ilike(f"%{q}%"),
            Medicine.generic_name.ilike(f"%{q}%")
        )
        query = query.filter(search_filter)
    
    if category_id:
        query = query.filter(Medicine.category_id == category_id)
    
    if prescription_required is not None:
        query = query.filter(Medicine.prescription_required == prescription_required)
    
    if min_price is not None:
        query = query.filter(Medicine.price >= min_price)
    
    if max_price is not None:
        query = query.filter(Medicine.price <= max_price)
    
    if in_stock:
        query = query.filter(Medicine.stock_quantity > 0)
    
    if manufacturer:
        query = query.filter(Medicine.manufacturer.ilike(f"%{manufacturer}%"))
    
    if dosage_form:
        query = query.filter(Medicine.dosage_form.ilike(f"%{dosage_form}%"))
    
    # Apply sorting
    if sort_by == "name":
        sort_column = Medicine.name
    elif sort_by == "price":
        sort_column = Medicine.price
    elif sort_by == "created_at":
        sort_column = Medicine.created_at
    else:
        sort_column = Medicine.name
    
    if sort_order == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    offset = (page - 1) * page_size
    medicines = query.offset(offset).limit(page_size).all()
    
    # Calculate total pages
    total_pages = math.ceil(total / page_size)
    
    return MedicineSearchResponse(
        medicines=[MedicineResponse.model_validate(med) for med in medicines],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.get("/", response_model=List[MedicineResponse])
def get_medicines(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
) -> List[MedicineResponse]:
    """
    Get all medicines with pagination
    """
    medicines = db.query(Medicine).options(joinedload(Medicine.category)).offset(skip).limit(limit).all()
    return [MedicineResponse.model_validate(med) for med in medicines]


@router.get("/{medicine_id}", response_model=MedicineResponse)
def get_medicine(
    medicine_id: str,
    db: Session = Depends(get_db)
) -> MedicineResponse:
    """
    Get a specific medicine by ID
    """
    medicine = db.query(Medicine).options(joinedload(Medicine.category)).filter(Medicine.id == medicine_id).first()
    if not medicine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medicine not found"
        )
    
    return MedicineResponse.model_validate(medicine)


@router.get("/{medicine_id}/alternatives", response_model=MedicineAlternatives)
def get_medicine_alternatives(
    medicine_id: str,
    db: Session = Depends(get_db)
) -> MedicineAlternatives:
    """
    Get alternative medicines for a specific medicine
    """
    medicine = db.query(Medicine).filter(Medicine.id == medicine_id).first()
    if not medicine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medicine not found"
        )
    
    # Find alternatives based on generic name or category
    alternatives_query = db.query(Medicine).filter(
        and_(
            Medicine.id != medicine_id,
            or_(
                Medicine.generic_name == medicine.generic_name,
                Medicine.category_id == medicine.category_id
            )
        )
    ).limit(10)
    
    alternatives = alternatives_query.all()
    
    return MedicineAlternatives(
        medicine_id=medicine_id,
        alternatives=[MedicineResponse.model_validate(alt) for alt in alternatives]
    )


@router.post("/", response_model=MedicineResponse, status_code=status.HTTP_201_CREATED)
def create_medicine(
    medicine_data: MedicineCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> MedicineResponse:
    """
    Create a new medicine (admin only)
    """
    # TODO: Add role-based access control for admin users
    
    # Check if category exists
    if medicine_data.category_id:
        category = db.query(Category).filter(Category.id == medicine_data.category_id).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category not found"
            )
    
    # Create new medicine
    new_medicine = Medicine(**medicine_data.model_dump())
    db.add(new_medicine)
    db.commit()
    db.refresh(new_medicine)
    
    # Load category for response
    medicine_with_category = db.query(Medicine).options(joinedload(Medicine.category)).filter(Medicine.id == new_medicine.id).first()
    
    return MedicineResponse.model_validate(medicine_with_category)


@router.put("/{medicine_id}", response_model=MedicineResponse)
def update_medicine(
    medicine_id: str,
    medicine_data: MedicineUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> MedicineResponse:
    """
    Update a medicine (admin only)
    """
    # TODO: Add role-based access control for admin users
    
    medicine = db.query(Medicine).filter(Medicine.id == medicine_id).first()
    if not medicine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medicine not found"
        )
    
    # Update medicine fields
    update_data = medicine_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(medicine, field, value)
    
    db.commit()
    db.refresh(medicine)
    
    # Load category for response
    medicine_with_category = db.query(Medicine).options(joinedload(Medicine.category)).filter(Medicine.id == medicine.id).first()
    
    return MedicineResponse.model_validate(medicine_with_category)


@router.patch("/{medicine_id}/stock")
def update_medicine_stock(
    medicine_id: str,
    stock_quantity: int = Query(..., ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> dict:
    """
    Update medicine stock quantity (admin only)
    """
    # TODO: Add role-based access control for admin users
    
    medicine = db.query(Medicine).filter(Medicine.id == medicine_id).first()
    if not medicine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medicine not found"
        )
    
    medicine.stock_quantity = stock_quantity
    db.commit()
    
    return {
        "message": "Stock updated successfully",
        "medicine_id": medicine_id,
        "new_stock_quantity": stock_quantity
    }


@router.delete("/{medicine_id}")
def delete_medicine(
    medicine_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> dict:
    """
    Delete a medicine (admin only)
    """
    # TODO: Add role-based access control for admin users
    
    medicine = db.query(Medicine).filter(Medicine.id == medicine_id).first()
    if not medicine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medicine not found"
        )
    
    db.delete(medicine)
    db.commit()
    
    return {"message": "Medicine deleted successfully"}
