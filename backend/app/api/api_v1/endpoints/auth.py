"""
Authentication endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.user import User
from app.models.cart import Cart
from app.schemas.user import UserCreate, UserLogin, UserResponse, UserWithTokens, PhoneVerification
from app.core.security import verify_password, get_password_hash, create_token_pair, verify_token
from typing import Dict, Any

router = APIRouter()
security = HTTPBearer()


@router.post("/register", response_model=UserWithTokens, status_code=status.HTTP_201_CREATED)
def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Register a new user with medical profile
    """
    # Check if user already exists
    existing_user = db.query(User).filter(
        (User.email == user_data.email) | (User.phone == user_data.phone)
    ).first()
    
    if existing_user:
        if existing_user.email == user_data.email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this phone number already exists"
            )
    
    # Hash password
    hashed_password = get_password_hash(user_data.password)
    
    # Create user
    new_user = User(
        email=user_data.email,
        phone=user_data.phone,
        password_hash=hashed_password,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        date_of_birth=user_data.date_of_birth,
        medical_conditions=user_data.medical_conditions,
        allergies=user_data.allergies,
        emergency_contact=user_data.emergency_contact.dict() if user_data.emergency_contact else None,
        delivery_addresses=[addr.dict() for addr in user_data.delivery_addresses] if user_data.delivery_addresses else None,
        phone_verified=False
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Create cart for user
    new_cart = Cart(user_id=new_user.id)
    db.add(new_cart)
    db.commit()
    
    # Generate tokens
    tokens = create_token_pair(new_user.id)
    
    return {
        "user": UserResponse.model_validate(new_user),
        "tokens": tokens
    }


@router.post("/login", response_model=UserWithTokens)
def login_user(
    login_data: UserLogin,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    User login with email and password
    """
    # Find user by email
    user = db.query(User).filter(User.email == login_data.email).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Verify password
    if not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Generate tokens
    tokens = create_token_pair(user.id)
    
    return {
        "user": UserResponse.model_validate(user),
        "tokens": tokens
    }


def get_current_user(
    token: str = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Get current authenticated user
    """
    # Extract token from Bearer scheme
    token_str = token.credentials

    # Verify token
    user_id = verify_token(token_str)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    # Get user from database
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return user


@router.get("/me", response_model=UserResponse)
def get_current_user_profile(
    current_user: User = Depends(get_current_user)
) -> UserResponse:
    """
    Get current user profile
    """
    return UserResponse.model_validate(current_user)


@router.post("/verify-phone")
def verify_phone_number(
    verification_data: PhoneVerification,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Verify phone number with OTP
    """
    # In a real implementation, you would verify the OTP with your SMS service
    # For demonstration, we'll accept '123456' as valid OTP
    if verification_data.otp != "123456":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid OTP"
        )

    # Find user by phone
    user = db.query(User).filter(User.phone == verification_data.phone).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Update phone verification status
    user.phone_verified = True
    db.commit()
    
    return {
        "message": "Phone number verified successfully",
        "phone_verified": True
    }
