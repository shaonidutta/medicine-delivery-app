"""
Order management endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, func, desc
from typing import List, Optional, Dict, Any
import math
from datetime import date, datetime, timedelta
from app.database.session import get_db
from app.models.order import Order, OrderItem
from app.models.cart import Cart, CartItem
from app.models.medicine import Medicine
from app.models.user import User
from app.schemas.order import (
    OrderCreate, OrderUpdate, OrderResponse, OrderSearchQuery, OrderSearchResponse,
    OrderStatusUpdate, OrderTrackingInfo, OrderStats, CreateOrderFromCart,
    OrderCancellation, OrderDeliveryUpdate, OrderStatus, PaymentStatus
)
from app.api.api_v1.endpoints.auth import get_current_user
from app.services.order_service import OrderService
from app.services.cart_service import CartService

router = APIRouter()


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> OrderResponse:
    """
    Create a new order directly
    """
    order_service = OrderService(db)
    return order_service.create_order(current_user.id, order_data)


@router.post("/from-cart", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order_from_cart(
    order_data: CreateOrderFromCart,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> OrderResponse:
    """
    Create an order from current cart items
    """
    order_service = OrderService(db)
    cart_service = CartService(db)
    
    # Validate cart if requested
    if order_data.validate_prescriptions:
        validation_result = cart_service.validate_cart(current_user.id)
        if not validation_result.is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "message": "Cart validation failed",
                    "errors": validation_result.errors,
                    "prescription_issues": validation_result.prescription_issues
                }
            )
    
    # Get cart items
    cart = cart_service.get_or_create_cart(current_user.id)
    cart_items = db.query(CartItem).options(joinedload(CartItem.medicine)).filter(
        CartItem.cart_id == cart.id
    ).all()
    
    if not cart_items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cart is empty"
        )
    
    # Create order from cart
    order = order_service.create_order_from_cart(current_user.id, cart_items, order_data)
    
    # Clear cart after successful order creation
    cart_service.clear_cart(current_user.id)
    
    return order


@router.get("/", response_model=List[OrderResponse])
def get_user_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    status_filter: Optional[OrderStatus] = Query(None, alias="status"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> List[OrderResponse]:
    """
    Get current user's orders
    """
    query = db.query(Order).options(joinedload(Order.items)).filter(
        Order.user_id == current_user.id
    )
    
    if status_filter:
        query = query.filter(Order.status == status_filter)
    
    orders = query.order_by(desc(Order.created_at)).offset(skip).limit(limit).all()
    
    return [OrderResponse.model_validate(order) for order in orders]


@router.get("/search", response_model=OrderSearchResponse)
def search_orders(
    status_filter: Optional[OrderStatus] = Query(None, alias="status"),
    payment_status: Optional[PaymentStatus] = Query(None),
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    delivery_partner_id: Optional[str] = Query(None),
    pharmacy_id: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> OrderSearchResponse:
    """
    Search orders with advanced filtering (admin only)
    """
    # TODO: Add role-based access control for admin users
    
    # Build query
    query = db.query(Order).options(joinedload(Order.items))
    
    # Apply filters
    if status_filter:
        query = query.filter(Order.status == status_filter)
    
    if payment_status:
        query = query.filter(Order.payment_status == payment_status)
    
    if date_from:
        query = query.filter(Order.created_at >= date_from)
    
    if date_to:
        query = query.filter(Order.created_at <= date_to + timedelta(days=1))
    
    if delivery_partner_id:
        query = query.filter(Order.delivery_partner_id == delivery_partner_id)
    
    if pharmacy_id:
        query = query.filter(Order.pharmacy_id == pharmacy_id)
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    offset = (page - 1) * page_size
    orders = query.order_by(desc(Order.created_at)).offset(offset).limit(page_size).all()
    
    # Calculate total pages
    total_pages = math.ceil(total / page_size)
    
    return OrderSearchResponse(
        orders=[OrderResponse.model_validate(order) for order in orders],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> OrderResponse:
    """
    Get a specific order by ID
    """
    order = db.query(Order).options(joinedload(Order.items)).filter(
        Order.id == order_id
    ).first()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    # Check if user owns the order or is admin
    if order.user_id != current_user.id:
        # TODO: Add role-based access control for admin users
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    return OrderResponse.model_validate(order)


@router.put("/{order_id}/status", response_model=OrderResponse)
def update_order_status(
    order_id: str,
    status_data: OrderStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> OrderResponse:
    """
    Update order status (admin/pharmacy only)
    """
    # TODO: Add role-based access control for admin/pharmacy users
    
    order_service = OrderService(db)
    return order_service.update_order_status(order_id, status_data, current_user.id)


@router.put("/{order_id}/delivery", response_model=OrderResponse)
def update_delivery_info(
    order_id: str,
    delivery_data: OrderDeliveryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> OrderResponse:
    """
    Update delivery information (admin/delivery partner only)
    """
    # TODO: Add role-based access control for admin/delivery partner users
    
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    # Update delivery information
    order.delivery_partner_id = delivery_data.delivery_partner_id
    order.estimated_delivery_time = delivery_data.estimated_delivery_time
    if delivery_data.tracking_number:
        order.tracking_number = delivery_data.tracking_number
    
    # Update status to shipped if not already
    if order.status in [OrderStatus.CONFIRMED, OrderStatus.PROCESSING, OrderStatus.PACKED]:
        order.status = OrderStatus.SHIPPED
    
    db.commit()
    db.refresh(order)
    
    return OrderResponse.model_validate(order)


@router.get("/{order_id}/tracking", response_model=OrderTrackingInfo)
def get_order_tracking(
    order_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> OrderTrackingInfo:
    """
    Get order tracking information
    """
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    # Check if user owns the order or is admin
    if order.user_id != current_user.id:
        # TODO: Add role-based access control for admin users
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    # Mock status history - in real implementation, this would come from a status_history table
    status_history = [
        {
            "status": "pending",
            "timestamp": order.created_at.isoformat(),
            "description": "Order placed successfully"
        },
        {
            "status": "confirmed",
            "timestamp": (order.created_at + timedelta(minutes=5)).isoformat(),
            "description": "Order confirmed by pharmacy"
        }
    ]
    
    if order.status in [OrderStatus.PROCESSING, OrderStatus.PACKED, OrderStatus.SHIPPED, OrderStatus.OUT_FOR_DELIVERY, OrderStatus.DELIVERED]:
        status_history.append({
            "status": "processing",
            "timestamp": (order.created_at + timedelta(minutes=15)).isoformat(),
            "description": "Order is being prepared"
        })
    
    if order.status in [OrderStatus.SHIPPED, OrderStatus.OUT_FOR_DELIVERY, OrderStatus.DELIVERED]:
        status_history.append({
            "status": "shipped",
            "timestamp": (order.created_at + timedelta(minutes=30)).isoformat(),
            "description": "Order picked up by delivery partner"
        })
    
    return OrderTrackingInfo(
        order_id=order.id,
        order_number=order.order_number,
        status=order.status,
        tracking_number=order.tracking_number,
        delivery_partner=order.delivery_partner_id,
        estimated_delivery_time=order.estimated_delivery_time,
        status_history=status_history,
        current_location="Mumbai Warehouse" if order.status == OrderStatus.SHIPPED else None,
        delivery_address=order.delivery_address
    )


@router.post("/{order_id}/cancel", response_model=OrderResponse)
def cancel_order(
    order_id: str,
    cancellation_data: OrderCancellation,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> OrderResponse:
    """
    Cancel an order
    """
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    # Check if user owns the order
    if order.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    # Check if order can be cancelled
    if order.status in [OrderStatus.DELIVERED, OrderStatus.CANCELLED, OrderStatus.RETURNED]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot cancel order with status: {order.status}"
        )
    
    # Cancel the order
    order.status = OrderStatus.CANCELLED
    order.cancellation_reason = cancellation_data.reason
    
    # Update payment status if refund is requested
    if cancellation_data.refund_requested and order.payment_status == PaymentStatus.COMPLETED:
        order.payment_status = PaymentStatus.REFUNDED
    
    db.commit()
    db.refresh(order)
    
    return OrderResponse.model_validate(order)


@router.get("/stats/overview", response_model=OrderStats)
def get_order_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> OrderStats:
    """
    Get order statistics (admin only)
    """
    # TODO: Add role-based access control for admin users
    
    # Get counts by status
    stats = db.query(
        func.count(Order.id).label('total'),
        func.sum(func.case((Order.status == OrderStatus.PENDING, 1), else_=0)).label('pending'),
        func.sum(func.case((Order.status == OrderStatus.CONFIRMED, 1), else_=0)).label('confirmed'),
        func.sum(func.case((Order.status == OrderStatus.PROCESSING, 1), else_=0)).label('processing'),
        func.sum(func.case((Order.status == OrderStatus.DELIVERED, 1), else_=0)).label('delivered'),
        func.sum(func.case((Order.status == OrderStatus.CANCELLED, 1), else_=0)).label('cancelled'),
        func.sum(Order.total_amount).label('total_revenue'),
        func.avg(Order.total_amount).label('avg_order_value')
    ).first()
    
    return OrderStats(
        total_orders=stats.total or 0,
        pending_orders=stats.pending or 0,
        confirmed_orders=stats.confirmed or 0,
        processing_orders=stats.processing or 0,
        delivered_orders=stats.delivered or 0,
        cancelled_orders=stats.cancelled or 0,
        total_revenue=float(stats.total_revenue or 0),
        average_order_value=float(stats.avg_order_value or 0)
    )
