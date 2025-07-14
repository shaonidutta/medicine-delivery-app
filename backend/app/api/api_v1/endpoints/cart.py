"""
Shopping cart management endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List, Dict, Any
from app.database.session import get_db
from app.models.cart import Cart, CartItem
from app.models.medicine import Medicine
from app.models.prescription import Prescription
from app.models.user import User
from app.schemas.cart import (
    CartResponse, CartItemResponse, AddToCartRequest, UpdateCartItemRequest,
    CartSummary, CartValidationResult, CartCheckoutRequest, BulkCartOperation,
    CartItemAvailability
)
from app.api.api_v1.endpoints.auth import get_current_user
from app.services.cart_service import CartService

router = APIRouter()


@router.get("/", response_model=CartResponse)
def get_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> CartResponse:
    """
    Get current user's cart with all items
    """
    cart_service = CartService(db)
    cart = cart_service.get_or_create_cart(current_user.id)
    
    # Load cart items with medicine details
    cart_items = db.query(CartItem).options(
        joinedload(CartItem.medicine)
    ).filter(CartItem.cart_id == cart.id).all()
    
    # Calculate totals
    subtotal = sum(item.quantity * item.medicine.price for item in cart_items)
    tax_amount = subtotal * 0.18  # 18% GST
    delivery_fee = 50.0 if subtotal < 500 else 0.0  # Free delivery above ₹500
    total_amount = subtotal + tax_amount + delivery_fee
    
    # Check for prescription items
    has_prescription_items = any(item.medicine.prescription_required for item in cart_items)
    
    # Build response
    cart_response = CartResponse(
        id=cart.id,
        user_id=cart.user_id,
        items=[
            CartItemResponse(
                id=item.id,
                cart_id=item.cart_id,
                medicine_id=item.medicine_id,
                quantity=item.quantity,
                prescription_id=item.prescription_id,
                notes=item.notes,
                unit_price=item.medicine.price,
                total_price=item.quantity * item.medicine.price,
                medicine={
                    "id": item.medicine.id,
                    "name": item.medicine.name,
                    "generic_name": item.medicine.generic_name,
                    "manufacturer": item.medicine.manufacturer,
                    "price": item.medicine.price,
                    "prescription_required": item.medicine.prescription_required,
                    "stock_quantity": item.medicine.stock_quantity
                },
                is_prescription_valid=cart_service.validate_prescription_for_item(item),
                created_at=item.created_at,
                updated_at=item.updated_at
            ) for item in cart_items
        ],
        total_items=len(cart_items),
        subtotal=subtotal,
        tax_amount=tax_amount,
        delivery_fee=delivery_fee,
        total_amount=total_amount,
        has_prescription_items=has_prescription_items,
        prescription_validation_status="valid",  # TODO: Implement proper validation
        created_at=cart.created_at,
        updated_at=cart.updated_at
    )
    
    return cart_response


@router.post("/items", response_model=CartItemResponse, status_code=status.HTTP_201_CREATED)
def add_to_cart(
    item_data: AddToCartRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> CartItemResponse:
    """
    Add an item to the cart
    """
    cart_service = CartService(db)
    
    # Get or create cart
    cart = cart_service.get_or_create_cart(current_user.id)
    
    # Get medicine
    medicine = db.query(Medicine).filter(Medicine.id == item_data.medicine_id).first()
    if not medicine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medicine not found"
        )
    
    # Check stock availability
    if medicine.stock_quantity < item_data.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient stock. Available: {medicine.stock_quantity}"
        )
    
    # Check prescription requirement
    if medicine.prescription_required and not item_data.prescription_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This medicine requires a valid prescription"
        )
    
    # Validate prescription if provided
    if item_data.prescription_id:
        prescription = db.query(Prescription).filter(
            Prescription.id == item_data.prescription_id,
            Prescription.user_id == current_user.id
        ).first()
        
        if not prescription:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Prescription not found"
            )
        
        if prescription.status != "verified":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Prescription must be verified before use"
            )
    
    # Check if item already exists in cart
    existing_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.medicine_id == item_data.medicine_id
    ).first()
    
    if existing_item:
        # Update quantity
        new_quantity = existing_item.quantity + item_data.quantity
        if new_quantity > medicine.stock_quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Total quantity would exceed available stock: {medicine.stock_quantity}"
            )
        
        existing_item.quantity = new_quantity
        existing_item.notes = item_data.notes or existing_item.notes
        if item_data.prescription_id:
            existing_item.prescription_id = item_data.prescription_id
        
        db.commit()
        db.refresh(existing_item)
        cart_item = existing_item
    else:
        # Create new cart item
        cart_item = CartItem(
            cart_id=cart.id,
            medicine_id=item_data.medicine_id,
            quantity=item_data.quantity,
            prescription_id=item_data.prescription_id,
            notes=item_data.notes
        )
        db.add(cart_item)
        db.commit()
        db.refresh(cart_item)
    
    # Load medicine details for response
    cart_item_with_medicine = db.query(CartItem).options(
        joinedload(CartItem.medicine)
    ).filter(CartItem.id == cart_item.id).first()
    
    return CartItemResponse(
        id=cart_item_with_medicine.id,
        cart_id=cart_item_with_medicine.cart_id,
        medicine_id=cart_item_with_medicine.medicine_id,
        quantity=cart_item_with_medicine.quantity,
        prescription_id=cart_item_with_medicine.prescription_id,
        notes=cart_item_with_medicine.notes,
        unit_price=cart_item_with_medicine.medicine.price,
        total_price=cart_item_with_medicine.quantity * cart_item_with_medicine.medicine.price,
        medicine={
            "id": cart_item_with_medicine.medicine.id,
            "name": cart_item_with_medicine.medicine.name,
            "generic_name": cart_item_with_medicine.medicine.generic_name,
            "manufacturer": cart_item_with_medicine.medicine.manufacturer,
            "price": cart_item_with_medicine.medicine.price,
            "prescription_required": cart_item_with_medicine.medicine.prescription_required,
            "stock_quantity": cart_item_with_medicine.medicine.stock_quantity
        },
        is_prescription_valid=True,  # TODO: Implement proper validation
        created_at=cart_item_with_medicine.created_at,
        updated_at=cart_item_with_medicine.updated_at
    )


@router.put("/items/{item_id}", response_model=CartItemResponse)
def update_cart_item(
    item_id: str,
    item_data: UpdateCartItemRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> CartItemResponse:
    """
    Update a cart item
    """
    # Get user's cart
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart not found"
        )
    
    # Get cart item
    cart_item = db.query(CartItem).options(joinedload(CartItem.medicine)).filter(
        CartItem.id == item_id,
        CartItem.cart_id == cart.id
    ).first()
    
    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found"
        )
    
    # Check stock availability
    if cart_item.medicine.stock_quantity < item_data.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient stock. Available: {cart_item.medicine.stock_quantity}"
        )
    
    # Update cart item
    cart_item.quantity = item_data.quantity
    if item_data.prescription_id:
        cart_item.prescription_id = item_data.prescription_id
    if item_data.notes:
        cart_item.notes = item_data.notes
    
    db.commit()
    db.refresh(cart_item)
    
    return CartItemResponse(
        id=cart_item.id,
        cart_id=cart_item.cart_id,
        medicine_id=cart_item.medicine_id,
        quantity=cart_item.quantity,
        prescription_id=cart_item.prescription_id,
        notes=cart_item.notes,
        unit_price=cart_item.medicine.price,
        total_price=cart_item.quantity * cart_item.medicine.price,
        medicine={
            "id": cart_item.medicine.id,
            "name": cart_item.medicine.name,
            "generic_name": cart_item.medicine.generic_name,
            "manufacturer": cart_item.medicine.manufacturer,
            "price": cart_item.medicine.price,
            "prescription_required": cart_item.medicine.prescription_required,
            "stock_quantity": cart_item.medicine.stock_quantity
        },
        is_prescription_valid=True,  # TODO: Implement proper validation
        created_at=cart_item.created_at,
        updated_at=cart_item.updated_at
    )


@router.delete("/items/{item_id}")
def remove_from_cart(
    item_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Dict[str, str]:
    """
    Remove an item from the cart
    """
    # Get user's cart
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart not found"
        )
    
    # Get and delete cart item
    cart_item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.cart_id == cart.id
    ).first()
    
    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found"
        )
    
    db.delete(cart_item)
    db.commit()
    
    return {"message": "Item removed from cart successfully"}


@router.delete("/clear")
def clear_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Dict[str, str]:
    """
    Clear all items from the cart
    """
    # Get user's cart
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart not found"
        )
    
    # Delete all cart items
    db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
    db.commit()
    
    return {"message": "Cart cleared successfully"}


@router.get("/summary", response_model=CartSummary)
def get_cart_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> CartSummary:
    """
    Get cart summary with totals
    """
    cart_service = CartService(db)
    cart = cart_service.get_or_create_cart(current_user.id)
    
    # Get cart items
    cart_items = db.query(CartItem).options(joinedload(CartItem.medicine)).filter(
        CartItem.cart_id == cart.id
    ).all()
    
    # Calculate totals
    subtotal = sum(item.quantity * item.medicine.price for item in cart_items)
    tax_amount = subtotal * 0.18  # 18% GST
    delivery_fee = 50.0 if subtotal < 500 else 0.0  # Free delivery above ₹500
    total_amount = subtotal + tax_amount + delivery_fee
    
    # Check for prescription items
    has_prescription_items = any(item.medicine.prescription_required for item in cart_items)
    
    return CartSummary(
        total_items=len(cart_items),
        subtotal=subtotal,
        tax_amount=tax_amount,
        delivery_fee=delivery_fee,
        total_amount=total_amount,
        has_prescription_items=has_prescription_items,
        prescription_validation_status="valid"  # TODO: Implement proper validation
    )


@router.post("/validate", response_model=CartValidationResult)
def validate_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> CartValidationResult:
    """
    Validate cart items for checkout
    """
    cart_service = CartService(db)
    return cart_service.validate_cart(current_user.id)
