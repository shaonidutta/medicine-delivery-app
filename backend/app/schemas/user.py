"""
User Pydantic schemas
"""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List, Dict, Any
from datetime import date, datetime
import re
import phonenumbers


class EmergencyContact(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    phone: str = Field(..., min_length=10, max_length=20)
    relationship: str = Field(..., min_length=2, max_length=50)


class DeliveryAddress(BaseModel):
    label: str = Field(..., min_length=1, max_length=50)
    address_line_1: str = Field(..., min_length=5, max_length=200)
    address_line_2: Optional[str] = Field(None, max_length=200)
    city: str = Field(..., min_length=2, max_length=100)
    state: str = Field(..., min_length=2, max_length=100)
    postal_code: str = Field(..., min_length=5, max_length=10)
    country: str = Field(default="India", max_length=50)
    is_default: bool = Field(default=False)


class UserCreate(BaseModel):
    email: EmailStr
    phone: str = Field(..., min_length=10, max_length=20)
    password: str = Field(..., min_length=8, max_length=100)
    first_name: str = Field(..., min_length=2, max_length=100)
    last_name: str = Field(..., min_length=2, max_length=100)
    date_of_birth: Optional[date] = None
    medical_conditions: Optional[List[str]] = None
    allergies: Optional[List[str]] = None
    emergency_contact: Optional[EmergencyContact] = None
    delivery_addresses: Optional[List[DeliveryAddress]] = None

    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one digit')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Password must contain at least one special character')
        return v

    @validator('phone')
    @classmethod
    def validate_phone(cls, v):
        try:
            # Parse phone number (assuming Indian numbers if no country code)
            if not v.startswith('+'):
                v = '+91' + v
            parsed = phonenumbers.parse(v, None)
            if not phonenumbers.is_valid_number(parsed):
                raise ValueError('Invalid phone number')
            return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
        except phonenumbers.NumberParseException:
            raise ValueError('Invalid phone number format')

    @validator('date_of_birth')
    @classmethod
    def validate_date_of_birth(cls, v):
        if v and v >= date.today():
            raise ValueError('Date of birth must be in the past')
        return v


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=1)


class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=2, max_length=100)
    last_name: Optional[str] = Field(None, min_length=2, max_length=100)
    date_of_birth: Optional[date] = None
    medical_conditions: Optional[List[str]] = None
    allergies: Optional[List[str]] = None
    emergency_contact: Optional[EmergencyContact] = None
    delivery_addresses: Optional[List[DeliveryAddress]] = None

    @validator('date_of_birth')
    @classmethod
    def validate_date_of_birth(cls, v):
        if v and v >= date.today():
            raise ValueError('Date of birth must be in the past')
        return v


class UserResponse(BaseModel):
    id: str
    email: str
    phone: str
    first_name: str
    last_name: str
    date_of_birth: Optional[date]
    phone_verified: bool
    medical_conditions: Optional[List[str]]
    allergies: Optional[List[str]]
    emergency_contact: Optional[Dict[str, Any]]
    delivery_addresses: Optional[List[Dict[str, Any]]]
    created_at: datetime

    class Config:
        orm_mode = True


class PhoneVerification(BaseModel):
    phone: str = Field(..., min_length=10, max_length=20)
    otp: str = Field(..., min_length=6, max_length=6, pattern=r'^\d{6}$')


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserWithTokens(BaseModel):
    user: UserResponse
    tokens: TokenResponse
