"""
Category management endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from app.database.session import get_db
from app.models.category import Category
from app.models.medicine import Medicine
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse, CategoryWithMedicineCount
from app.api.api_v1.endpoints.auth import get_current_user
from app.models.user import User

router = APIRouter()


@router.get("/", response_model=List[CategoryResponse])
def get_categories(
    include_subcategories: bool = True,
    db: Session = Depends(get_db)
) -> List[CategoryResponse]:
    """
    Get all categories with optional subcategories
    """
    if include_subcategories:
        # Get root categories (no parent)
        categories = db.query(Category).filter(Category.parent_category_id.is_(None)).all()
        
        # Load subcategories for each root category
        for category in categories:
            category.subcategories = db.query(Category).filter(
                Category.parent_category_id == category.id
            ).all()
    else:
        categories = db.query(Category).all()
    
    return [CategoryResponse.model_validate(cat) for cat in categories]


@router.get("/with-counts", response_model=List[CategoryWithMedicineCount])
def get_categories_with_medicine_counts(
    db: Session = Depends(get_db)
) -> List[CategoryWithMedicineCount]:
    """
    Get all categories with medicine counts
    """
    # Query categories with medicine counts
    categories_with_counts = db.query(
        Category,
        func.count(Medicine.id).label('medicine_count')
    ).outerjoin(Medicine).group_by(Category.id).all()
    
    result = []
    for category, count in categories_with_counts:
        category_dict = CategoryResponse.model_validate(category).model_dump()
        category_dict['medicine_count'] = count
        result.append(CategoryWithMedicineCount(**category_dict))
    
    return result


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(
    category_id: str,
    db: Session = Depends(get_db)
) -> CategoryResponse:
    """
    Get a specific category by ID
    """
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    # Load subcategories
    category.subcategories = db.query(Category).filter(
        Category.parent_category_id == category.id
    ).all()
    
    return CategoryResponse.model_validate(category)


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    category_data: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> CategoryResponse:
    """
    Create a new category (admin only)
    """
    # TODO: Add role-based access control for admin users
    
    # Check if parent category exists
    if category_data.parent_category_id:
        parent = db.query(Category).filter(Category.id == category_data.parent_category_id).first()
        if not parent:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Parent category not found"
            )
    
    # Check if category name already exists
    existing_category = db.query(Category).filter(Category.name == category_data.name).first()
    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Category with this name already exists"
        )
    
    # Create new category
    new_category = Category(**category_data.model_dump())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    
    return CategoryResponse.model_validate(new_category)


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: str,
    category_data: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> CategoryResponse:
    """
    Update a category (admin only)
    """
    # TODO: Add role-based access control for admin users
    
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    # Update category fields
    update_data = category_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(category, field, value)
    
    db.commit()
    db.refresh(category)
    
    return CategoryResponse.model_validate(category)


@router.delete("/{category_id}")
def delete_category(
    category_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> dict:
    """
    Delete a category (admin only)
    """
    # TODO: Add role-based access control for admin users
    
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    # Check if category has medicines
    medicine_count = db.query(Medicine).filter(Medicine.category_id == category_id).count()
    if medicine_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot delete category with {medicine_count} medicines. Move medicines to another category first."
        )
    
    # Check if category has subcategories
    subcategory_count = db.query(Category).filter(Category.parent_category_id == category_id).count()
    if subcategory_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot delete category with {subcategory_count} subcategories. Delete subcategories first."
        )
    
    db.delete(category)
    db.commit()
    
    return {"message": "Category deleted successfully"}
