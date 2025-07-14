"""
Prescription Pydantic schemas
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from enum import Enum


class PrescriptionStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    VERIFIED = "verified"
    REJECTED = "rejected"
    EXPIRED = "expired"


class PrescriptionBase(BaseModel):
    doctor_name: str = Field(..., min_length=1, max_length=255)
    doctor_license: Optional[str] = Field(None, max_length=100)
    patient_name: str = Field(..., min_length=1, max_length=255)
    patient_age: Optional[int] = Field(None, ge=0, le=150)
    patient_gender: Optional[str] = Field(None, max_length=10)
    diagnosis: Optional[str] = Field(None, max_length=500)
    prescribed_medicines: List[Dict[str, Any]] = Field(default_factory=list)
    dosage_instructions: Optional[str] = Field(None, max_length=1000)
    prescription_date: date = Field(...)
    valid_until: Optional[date] = None
    notes: Optional[str] = Field(None, max_length=1000)

    @validator('prescription_date')
    @classmethod
    def validate_prescription_date(cls, v):
        if v > date.today():
            raise ValueError('Prescription date cannot be in the future')
        return v

    @validator('valid_until')
    @classmethod
    def validate_valid_until(cls, v, values):
        if v and 'prescription_date' in values:
            if v <= values['prescription_date']:
                raise ValueError('Valid until date must be after prescription date')
        return v


class PrescriptionCreate(PrescriptionBase):
    image_url: str = Field(..., description="URL of the uploaded prescription image")


class PrescriptionUpdate(BaseModel):
    doctor_name: Optional[str] = Field(None, min_length=1, max_length=255)
    doctor_license: Optional[str] = Field(None, max_length=100)
    patient_name: Optional[str] = Field(None, min_length=1, max_length=255)
    patient_age: Optional[int] = Field(None, ge=0, le=150)
    patient_gender: Optional[str] = Field(None, max_length=10)
    diagnosis: Optional[str] = Field(None, max_length=500)
    prescribed_medicines: Optional[List[Dict[str, Any]]] = None
    dosage_instructions: Optional[str] = Field(None, max_length=1000)
    prescription_date: Optional[date] = None
    valid_until: Optional[date] = None
    notes: Optional[str] = Field(None, max_length=1000)
    status: Optional[PrescriptionStatus] = None


class PrescriptionResponse(PrescriptionBase):
    id: str
    user_id: str
    image_url: str
    status: PrescriptionStatus
    verified_by: Optional[str] = None
    verification_notes: Optional[str] = None
    ocr_text: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class PrescriptionVerification(BaseModel):
    status: PrescriptionStatus = Field(..., description="New verification status")
    verification_notes: Optional[str] = Field(None, max_length=1000, description="Pharmacist verification notes")
    prescribed_medicines: Optional[List[Dict[str, Any]]] = Field(None, description="Verified medicine list")


class PrescriptionUpload(BaseModel):
    doctor_name: str = Field(..., min_length=1, max_length=255)
    patient_name: str = Field(..., min_length=1, max_length=255)
    prescription_date: date = Field(...)
    notes: Optional[str] = Field(None, max_length=1000)

    @validator('prescription_date')
    @classmethod
    def validate_prescription_date(cls, v):
        if v > date.today():
            raise ValueError('Prescription date cannot be in the future')
        return v


class OCRResult(BaseModel):
    text: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    extracted_medicines: List[Dict[str, Any]] = Field(default_factory=list)
    doctor_name: Optional[str] = None
    patient_name: Optional[str] = None
    prescription_date: Optional[date] = None


class PrescriptionSearchQuery(BaseModel):
    status: Optional[PrescriptionStatus] = Field(None, description="Filter by status")
    doctor_name: Optional[str] = Field(None, description="Filter by doctor name")
    patient_name: Optional[str] = Field(None, description="Filter by patient name")
    date_from: Optional[date] = Field(None, description="Filter prescriptions from this date")
    date_to: Optional[date] = Field(None, description="Filter prescriptions until this date")
    verified_by: Optional[str] = Field(None, description="Filter by verifying pharmacist")
    page: int = Field(1, ge=1, description="Page number")
    page_size: int = Field(20, ge=1, le=100, description="Items per page")


class PrescriptionSearchResponse(BaseModel):
    prescriptions: List[PrescriptionResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class PrescriptionStats(BaseModel):
    total_prescriptions: int
    pending_verification: int
    verified_prescriptions: int
    rejected_prescriptions: int
    expired_prescriptions: int
