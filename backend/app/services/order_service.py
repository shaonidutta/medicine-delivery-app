"""
Order service for business logic
"""

from sqlalchemy.orm import Session, joinedload
from typing import List, Dict, Any, Optional
from datetime import date, datetime, timedelta
import uuid
from app.models.order import Order, OrderItem
from app.models.cart import CartItem
from app.models.medicine import Medicine
from app.models.user import User
from app.schemas.order import (
    OrderCreate, OrderResponse, OrderStatusUpdate, CreateOrderFromCart,
    OrderStatus, PaymentStatus
)
from fastapi import HTTPException, status


class OrderService:
    """Service class for order operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def generate_order_number(self) -> str:
        """
        Generate a unique order number
        
        Returns:
            str: Unique order number
        """
        # Format: ORD-YYYYMMDD-XXXX (where XXXX is a random 4-digit number)
        today = datetime.now().strftime("%Y%m%d")
        random_suffix = str(uuid.uuid4().int)[:4]
        return f"ORD-{today}-{random_suffix}"
    
    def create_order(self, user_id: str, order_data: OrderCreate) -> OrderResponse:
        """
        Create a new order
        
        Args:
            user_id: User ID
            order_data: Order creation data
            
        Returns:
            OrderResponse: Created order
        """
        # Validate medicines and calculate totals
        subtotal = 0.0
        validated_items = []
        
        for item_data in order_data.items:
            medicine = self.db.query(Medicine).filter(
                Medicine.id == item_data.medicine_id
            ).first()
            
            if not medicine:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Medicine not found: {item_data.medicine_id}"
                )
            
            # Check stock availability
            if medicine.stock_quantity < item_data.quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Insufficient stock for {medicine.name}. Available: {medicine.stock_quantity}"
                )
            
            # Check prescription requirement
            if medicine.prescription_required and not item_data.prescription_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Prescription required for {medicine.name}"
                )
            
            item_total = item_data.quantity * medicine.price
            subtotal += item_total
            
            validated_items.append({
                "medicine": medicine,
                "item_data": item_data,
                "item_total": item_total
            })
        
        # Calculate totals
        tax_amount = subtotal * 0.18  # 18% GST
        delivery_fee = 50.0 if subtotal < 500 else 0.0
        total_amount = subtotal + tax_amount + delivery_fee
        
        # Create order
        order = Order(
            user_id=user_id,
            order_number=self.generate_order_number(),
            status=OrderStatus.PENDING,
            payment_status=PaymentStatus.PENDING,
            payment_method=order_data.payment_method,
            delivery_address=order_data.delivery_address.model_dump(),
            delivery_instructions=order_data.delivery_instructions,
            subtotal=subtotal,
            tax_amount=tax_amount,
            delivery_fee=delivery_fee,
            total_amount=total_amount,
            expected_delivery_date=order_data.expected_delivery_date,
            estimated_delivery_time=30  # Default 30 minutes
        )
        
        self.db.add(order)
        self.db.flush()  # Get order ID
        
        # Create order items and update stock
        for item_info in validated_items:
            medicine = item_info["medicine"]
            item_data = item_info["item_data"]
            
            order_item = OrderItem(
                order_id=order.id,
                medicine_id=item_data.medicine_id,
                quantity=item_data.quantity,
                unit_price=medicine.price,
                total_price=item_info["item_total"],
                prescription_id=item_data.prescription_id
            )
            
            self.db.add(order_item)
            
            # Update medicine stock
            medicine.stock_quantity -= item_data.quantity
        
        self.db.commit()
        self.db.refresh(order)
        
        # Load order with items for response
        order_with_items = self.db.query(Order).options(
            joinedload(Order.items)
        ).filter(Order.id == order.id).first()
        
        return OrderResponse.model_validate(order_with_items)
    
    def create_order_from_cart(
        self, 
        user_id: str, 
        cart_items: List[CartItem], 
        order_data: CreateOrderFromCart
    ) -> OrderResponse:
        """
        Create an order from cart items
        
        Args:
            user_id: User ID
            cart_items: List of cart items
            order_data: Order creation data
            
        Returns:
            OrderResponse: Created order
        """
        # Calculate totals
        subtotal = sum(item.quantity * item.medicine.price for item in cart_items)
        tax_amount = subtotal * 0.18  # 18% GST
        delivery_fee = 50.0 if subtotal < 500 else 0.0
        total_amount = subtotal + tax_amount + delivery_fee
        
        # Create order
        order = Order(
            user_id=user_id,
            order_number=self.generate_order_number(),
            status=OrderStatus.PENDING,
            payment_status=PaymentStatus.PENDING,
            payment_method=order_data.payment_method,
            delivery_address=order_data.delivery_address.model_dump(),
            delivery_instructions=order_data.delivery_instructions,
            subtotal=subtotal,
            tax_amount=tax_amount,
            delivery_fee=delivery_fee,
            total_amount=total_amount,
            estimated_delivery_time=30  # Default 30 minutes
        )
        
        self.db.add(order)
        self.db.flush()  # Get order ID
        
        # Create order items from cart items and update stock
        for cart_item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                medicine_id=cart_item.medicine_id,
                quantity=cart_item.quantity,
                unit_price=cart_item.medicine.price,
                total_price=cart_item.quantity * cart_item.medicine.price,
                prescription_id=cart_item.prescription_id
            )
            
            self.db.add(order_item)
            
            # Update medicine stock
            cart_item.medicine.stock_quantity -= cart_item.quantity
        
        self.db.commit()
        self.db.refresh(order)
        
        # Load order with items for response
        order_with_items = self.db.query(Order).options(
            joinedload(Order.items)
        ).filter(Order.id == order.id).first()
        
        return OrderResponse.model_validate(order_with_items)
    
    def update_order_status(
        self, 
        order_id: str, 
        status_data: OrderStatusUpdate, 
        updated_by: str
    ) -> OrderResponse:
        """
        Update order status
        
        Args:
            order_id: Order ID
            status_data: Status update data
            updated_by: User ID who is updating the status
            
        Returns:
            OrderResponse: Updated order
        """
        order = self.db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
        
        # Validate status transition
        if not self._is_valid_status_transition(order.status, status_data.status):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid status transition from {order.status} to {status_data.status}"
            )
        
        # Update order status
        old_status = order.status
        order.status = status_data.status
        
        if status_data.estimated_delivery_time:
            order.estimated_delivery_time = status_data.estimated_delivery_time
        
        # Update delivery date if delivered
        if status_data.status == OrderStatus.DELIVERED:
            order.actual_delivery_date = date.today()
            order.payment_status = PaymentStatus.COMPLETED
        
        # Update payment status based on order status
        if status_data.status == OrderStatus.CONFIRMED:
            order.payment_status = PaymentStatus.PROCESSING
        
        self.db.commit()
        self.db.refresh(order)
        
        # TODO: Add status history tracking
        # TODO: Send notifications to user
        
        # Load order with items for response
        order_with_items = self.db.query(Order).options(
            joinedload(Order.items)
        ).filter(Order.id == order.id).first()
        
        return OrderResponse.model_validate(order_with_items)
    
    def _is_valid_status_transition(self, current_status: OrderStatus, new_status: OrderStatus) -> bool:
        """
        Check if status transition is valid
        
        Args:
            current_status: Current order status
            new_status: New order status
            
        Returns:
            bool: True if transition is valid
        """
        # Define valid transitions
        valid_transitions = {
            OrderStatus.PENDING: [OrderStatus.CONFIRMED, OrderStatus.CANCELLED],
            OrderStatus.CONFIRMED: [OrderStatus.PROCESSING, OrderStatus.CANCELLED],
            OrderStatus.PROCESSING: [OrderStatus.PACKED, OrderStatus.CANCELLED],
            OrderStatus.PACKED: [OrderStatus.SHIPPED, OrderStatus.CANCELLED],
            OrderStatus.SHIPPED: [OrderStatus.OUT_FOR_DELIVERY, OrderStatus.RETURNED],
            OrderStatus.OUT_FOR_DELIVERY: [OrderStatus.DELIVERED, OrderStatus.RETURNED],
            OrderStatus.DELIVERED: [OrderStatus.RETURNED],
            OrderStatus.CANCELLED: [],  # Terminal state
            OrderStatus.RETURNED: []   # Terminal state
        }
        
        return new_status in valid_transitions.get(current_status, [])
    
    def get_order_by_id(self, order_id: str, user_id: Optional[str] = None) -> Optional[Order]:
        """
        Get order by ID with optional user validation
        
        Args:
            order_id: Order ID
            user_id: User ID for validation (optional)
            
        Returns:
            Order: Order object or None if not found
        """
        query = self.db.query(Order).options(joinedload(Order.items)).filter(
            Order.id == order_id
        )
        
        if user_id:
            query = query.filter(Order.user_id == user_id)
        
        return query.first()
    
    def get_user_orders(
        self, 
        user_id: str, 
        status_filter: Optional[OrderStatus] = None,
        limit: int = 20,
        offset: int = 0
    ) -> List[Order]:
        """
        Get user's orders with optional filtering
        
        Args:
            user_id: User ID
            status_filter: Optional status filter
            limit: Number of orders to return
            offset: Number of orders to skip
            
        Returns:
            List[Order]: List of orders
        """
        query = self.db.query(Order).options(joinedload(Order.items)).filter(
            Order.user_id == user_id
        )
        
        if status_filter:
            query = query.filter(Order.status == status_filter)
        
        return query.order_by(Order.created_at.desc()).offset(offset).limit(limit).all()
    
    def calculate_estimated_delivery_time(self, order: Order) -> int:
        """
        Calculate estimated delivery time based on order details
        
        Args:
            order: Order object
            
        Returns:
            int: Estimated delivery time in minutes
        """
        # Base delivery time
        base_time = 30  # 30 minutes base
        
        # Add time based on number of items
        item_count = len(order.items) if hasattr(order, 'items') else 1
        additional_time = min(item_count * 2, 20)  # Max 20 minutes additional
        
        # Add time for prescription items
        prescription_items = sum(1 for item in order.items if item.prescription_id) if hasattr(order, 'items') else 0
        prescription_time = prescription_items * 5  # 5 minutes per prescription item
        
        total_time = base_time + additional_time + prescription_time
        
        # Cap at 60 minutes for quick commerce
        return min(total_time, 60)
