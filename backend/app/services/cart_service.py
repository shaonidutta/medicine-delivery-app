"""
Cart service for business logic
"""

from sqlalchemy.orm import Session, joinedload
from typing import List, Dict, Any, Optional
from datetime import date, datetime, timedelta
from app.models.cart import Cart, CartItem
from app.models.medicine import Medicine
from app.models.prescription import Prescription
from app.models.user import User
from app.schemas.cart import CartValidationResult


class CartService:
    """Service class for cart operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_or_create_cart(self, user_id: str) -> Cart:
        """
        Get existing cart or create a new one for the user
        
        Args:
            user_id: User ID
            
        Returns:
            Cart: User's cart
        """
        cart = self.db.query(Cart).filter(Cart.user_id == user_id).first()
        
        if not cart:
            cart = Cart(user_id=user_id)
            self.db.add(cart)
            self.db.commit()
            self.db.refresh(cart)
        
        return cart
    
    def validate_prescription_for_item(self, cart_item: CartItem) -> bool:
        """
        Validate prescription for a cart item
        
        Args:
            cart_item: Cart item to validate
            
        Returns:
            bool: True if prescription is valid or not required
        """
        # Load medicine if not already loaded
        if not hasattr(cart_item, 'medicine') or cart_item.medicine is None:
            cart_item.medicine = self.db.query(Medicine).filter(
                Medicine.id == cart_item.medicine_id
            ).first()
        
        # If medicine doesn't require prescription, it's valid
        if not cart_item.medicine.prescription_required:
            return True
        
        # If prescription is required but not provided, it's invalid
        if not cart_item.prescription_id:
            return False
        
        # Check if prescription exists and is valid
        prescription = self.db.query(Prescription).filter(
            Prescription.id == cart_item.prescription_id
        ).first()
        
        if not prescription:
            return False
        
        # Check prescription status
        if prescription.status != "verified":
            return False
        
        # Check if prescription is expired
        if prescription.valid_until and prescription.valid_until < date.today():
            return False
        
        # Check if prescription contains the medicine
        if prescription.prescribed_medicines:
            prescribed_medicine_names = [
                med.get("name", "").lower() 
                for med in prescription.prescribed_medicines
            ]
            
            medicine_name = cart_item.medicine.name.lower()
            generic_name = (cart_item.medicine.generic_name or "").lower()
            
            if medicine_name not in prescribed_medicine_names and generic_name not in prescribed_medicine_names:
                return False
        
        return True
    
    def validate_cart(self, user_id: str) -> CartValidationResult:
        """
        Validate entire cart for checkout
        
        Args:
            user_id: User ID
            
        Returns:
            CartValidationResult: Validation result with errors and warnings
        """
        cart = self.get_or_create_cart(user_id)
        
        # Get all cart items with medicine details
        cart_items = self.db.query(CartItem).options(
            joinedload(CartItem.medicine)
        ).filter(CartItem.cart_id == cart.id).all()
        
        errors = []
        warnings = []
        prescription_issues = []
        
        if not cart_items:
            errors.append("Cart is empty")
            return CartValidationResult(
                is_valid=False,
                errors=errors,
                warnings=warnings,
                prescription_issues=prescription_issues
            )
        
        for item in cart_items:
            medicine = item.medicine
            
            # Check stock availability
            if medicine.stock_quantity < item.quantity:
                errors.append(
                    f"{medicine.name}: Insufficient stock. Available: {medicine.stock_quantity}, Requested: {item.quantity}"
                )
            
            # Check if medicine is expired
            if medicine.expiry_date and medicine.expiry_date <= date.today():
                errors.append(f"{medicine.name}: Medicine has expired")
            
            # Check prescription requirements
            if medicine.prescription_required:
                if not item.prescription_id:
                    prescription_issues.append({
                        "medicine_id": medicine.id,
                        "medicine_name": medicine.name,
                        "issue": "Prescription required but not provided",
                        "severity": "error"
                    })
                    errors.append(f"{medicine.name}: Prescription required")
                else:
                    # Validate prescription
                    prescription = self.db.query(Prescription).filter(
                        Prescription.id == item.prescription_id
                    ).first()
                    
                    if not prescription:
                        prescription_issues.append({
                            "medicine_id": medicine.id,
                            "medicine_name": medicine.name,
                            "issue": "Prescription not found",
                            "severity": "error"
                        })
                        errors.append(f"{medicine.name}: Prescription not found")
                    elif prescription.status != "verified":
                        prescription_issues.append({
                            "medicine_id": medicine.id,
                            "medicine_name": medicine.name,
                            "issue": f"Prescription status: {prescription.status}",
                            "severity": "error"
                        })
                        errors.append(f"{medicine.name}: Prescription not verified")
                    elif prescription.valid_until and prescription.valid_until < date.today():
                        prescription_issues.append({
                            "medicine_id": medicine.id,
                            "medicine_name": medicine.name,
                            "issue": "Prescription expired",
                            "severity": "error"
                        })
                        errors.append(f"{medicine.name}: Prescription expired")
            
            # Check for warnings
            if medicine.stock_quantity <= medicine.min_stock_level:
                warnings.append(f"{medicine.name}: Low stock warning")
            
            # Check expiry date warning (within 30 days)
            if medicine.expiry_date:
                days_to_expiry = (medicine.expiry_date - date.today()).days
                if 0 < days_to_expiry <= 30:
                    warnings.append(f"{medicine.name}: Expires in {days_to_expiry} days")
        
        return CartValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            prescription_issues=prescription_issues
        )
    
    def calculate_cart_totals(self, user_id: str) -> Dict[str, float]:
        """
        Calculate cart totals
        
        Args:
            user_id: User ID
            
        Returns:
            dict: Cart totals
        """
        cart = self.get_or_create_cart(user_id)
        
        cart_items = self.db.query(CartItem).options(
            joinedload(CartItem.medicine)
        ).filter(CartItem.cart_id == cart.id).all()
        
        subtotal = sum(item.quantity * item.medicine.price for item in cart_items)
        tax_rate = 0.18  # 18% GST
        tax_amount = subtotal * tax_rate
        
        # Delivery fee logic
        delivery_fee = 0.0
        if subtotal > 0:
            if subtotal < 500:
                delivery_fee = 50.0  # ₹50 delivery fee for orders below ₹500
            else:
                delivery_fee = 0.0  # Free delivery for orders ₹500 and above
        
        total_amount = subtotal + tax_amount + delivery_fee
        
        return {
            "subtotal": subtotal,
            "tax_amount": tax_amount,
            "delivery_fee": delivery_fee,
            "total_amount": total_amount,
            "tax_rate": tax_rate
        }
    
    def get_cart_item_count(self, user_id: str) -> int:
        """
        Get total number of items in cart
        
        Args:
            user_id: User ID
            
        Returns:
            int: Number of items in cart
        """
        cart = self.get_or_create_cart(user_id)
        return self.db.query(CartItem).filter(CartItem.cart_id == cart.id).count()
    
    def clear_cart(self, user_id: str) -> bool:
        """
        Clear all items from cart
        
        Args:
            user_id: User ID
            
        Returns:
            bool: True if successful
        """
        try:
            cart = self.get_or_create_cart(user_id)
            self.db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
            self.db.commit()
            return True
        except Exception:
            self.db.rollback()
            return False
    
    def update_item_quantity(self, user_id: str, item_id: str, quantity: int) -> bool:
        """
        Update quantity of a cart item
        
        Args:
            user_id: User ID
            item_id: Cart item ID
            quantity: New quantity
            
        Returns:
            bool: True if successful
        """
        try:
            cart = self.get_or_create_cart(user_id)
            
            cart_item = self.db.query(CartItem).filter(
                CartItem.id == item_id,
                CartItem.cart_id == cart.id
            ).first()
            
            if not cart_item:
                return False
            
            # Check stock availability
            medicine = self.db.query(Medicine).filter(
                Medicine.id == cart_item.medicine_id
            ).first()
            
            if medicine.stock_quantity < quantity:
                return False
            
            cart_item.quantity = quantity
            self.db.commit()
            return True
            
        except Exception:
            self.db.rollback()
            return False
