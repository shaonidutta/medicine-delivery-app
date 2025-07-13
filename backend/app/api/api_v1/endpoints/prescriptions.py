"""
Prescription management endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from typing import List, Optional
import math
from datetime import date, datetime
from app.database.session import get_db
from app.models.prescription import Prescription
from app.models.user import User
from app.schemas.prescription import (
    PrescriptionCreate, PrescriptionUpdate, PrescriptionResponse,
    PrescriptionVerification, PrescriptionUpload, OCRResult,
    PrescriptionSearchQuery, PrescriptionSearchResponse, PrescriptionStats,
    PrescriptionStatus
)
from app.api.api_v1.endpoints.auth import get_current_user
from app.services.file_upload import upload_file
from app.services.ocr_service import extract_text_from_image

router = APIRouter()


@router.post("/upload", response_model=PrescriptionResponse, status_code=status.HTTP_201_CREATED)
def upload_prescription(
    file: UploadFile = File(..., description="Prescription image file"),
    doctor_name: str = Form(..., description="Doctor's name"),
    patient_name: str = Form(..., description="Patient's name"),
    prescription_date: date = Form(..., description="Prescription date"),
    notes: Optional[str] = Form(None, description="Additional notes"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> PrescriptionResponse:
    """
    Upload a prescription image and create a prescription record
    """
    # Validate file type
    if not file.content_type or not file.content_type.startswith('image/'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only image files are allowed"
        )
    
    # Upload file to storage (mock implementation)
    try:
        image_url = upload_file(file, "prescriptions")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload file: {str(e)}"
        )
    
    # Extract text using OCR (mock implementation)
    try:
        ocr_result = extract_text_from_image(image_url)
        ocr_text = ocr_result.get("text", "")
    except Exception as e:
        ocr_text = f"OCR processing failed: {str(e)}"
    
    # Create prescription record
    prescription_data = {
        "user_id": current_user.id,
        "doctor_name": doctor_name,
        "patient_name": patient_name,
        "prescription_date": prescription_date,
        "notes": notes,
        "image_url": image_url,
        "ocr_text": ocr_text,
        "status": PrescriptionStatus.PENDING
    }
    
    new_prescription = Prescription(**prescription_data)
    db.add(new_prescription)
    db.commit()
    db.refresh(new_prescription)
    
    return PrescriptionResponse.model_validate(new_prescription)


@router.get("/", response_model=List[PrescriptionResponse])
def get_user_prescriptions(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    status_filter: Optional[PrescriptionStatus] = Query(None, alias="status"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> List[PrescriptionResponse]:
    """
    Get current user's prescriptions
    """
    query = db.query(Prescription).filter(Prescription.user_id == current_user.id)
    
    if status_filter:
        query = query.filter(Prescription.status == status_filter)
    
    prescriptions = query.order_by(Prescription.created_at.desc()).offset(skip).limit(limit).all()
    
    return [PrescriptionResponse.model_validate(p) for p in prescriptions]


@router.get("/search", response_model=PrescriptionSearchResponse)
def search_prescriptions(
    status_filter: Optional[PrescriptionStatus] = Query(None, alias="status"),
    doctor_name: Optional[str] = Query(None),
    patient_name: Optional[str] = Query(None),
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    verified_by: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> PrescriptionSearchResponse:
    """
    Search prescriptions with advanced filtering (admin/pharmacist only)
    """
    # TODO: Add role-based access control for admin/pharmacist users
    
    # Build query
    query = db.query(Prescription)
    
    # Apply filters
    if status_filter:
        query = query.filter(Prescription.status == status_filter)
    
    if doctor_name:
        query = query.filter(Prescription.doctor_name.ilike(f"%{doctor_name}%"))
    
    if patient_name:
        query = query.filter(Prescription.patient_name.ilike(f"%{patient_name}%"))
    
    if date_from:
        query = query.filter(Prescription.prescription_date >= date_from)
    
    if date_to:
        query = query.filter(Prescription.prescription_date <= date_to)
    
    if verified_by:
        query = query.filter(Prescription.verified_by == verified_by)
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    offset = (page - 1) * page_size
    prescriptions = query.order_by(Prescription.created_at.desc()).offset(offset).limit(page_size).all()
    
    # Calculate total pages
    total_pages = math.ceil(total / page_size)
    
    return PrescriptionSearchResponse(
        prescriptions=[PrescriptionResponse.model_validate(p) for p in prescriptions],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.get("/{prescription_id}", response_model=PrescriptionResponse)
def get_prescription(
    prescription_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> PrescriptionResponse:
    """
    Get a specific prescription by ID
    """
    prescription = db.query(Prescription).filter(Prescription.id == prescription_id).first()
    if not prescription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prescription not found"
        )
    
    # Check if user owns the prescription or is admin/pharmacist
    if prescription.user_id != current_user.id:
        # TODO: Add role-based access control for admin/pharmacist users
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    return PrescriptionResponse.model_validate(prescription)


@router.put("/{prescription_id}/verify", response_model=PrescriptionResponse)
def verify_prescription(
    prescription_id: str,
    verification_data: PrescriptionVerification,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> PrescriptionResponse:
    """
    Verify a prescription (pharmacist only)
    """
    # TODO: Add role-based access control for pharmacist users
    
    prescription = db.query(Prescription).filter(Prescription.id == prescription_id).first()
    if not prescription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prescription not found"
        )
    
    # Update prescription with verification data
    prescription.status = verification_data.status
    prescription.verified_by = current_user.id
    prescription.verification_notes = verification_data.verification_notes
    
    if verification_data.prescribed_medicines:
        prescription.prescribed_medicines = verification_data.prescribed_medicines
    
    db.commit()
    db.refresh(prescription)
    
    return PrescriptionResponse.model_validate(prescription)


@router.put("/{prescription_id}", response_model=PrescriptionResponse)
def update_prescription(
    prescription_id: str,
    prescription_data: PrescriptionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> PrescriptionResponse:
    """
    Update a prescription (owner or admin only)
    """
    prescription = db.query(Prescription).filter(Prescription.id == prescription_id).first()
    if not prescription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prescription not found"
        )
    
    # Check if user owns the prescription or is admin
    if prescription.user_id != current_user.id:
        # TODO: Add role-based access control for admin users
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    # Update prescription fields
    update_data = prescription_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(prescription, field, value)
    
    db.commit()
    db.refresh(prescription)
    
    return PrescriptionResponse.model_validate(prescription)


@router.delete("/{prescription_id}")
def delete_prescription(
    prescription_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> dict:
    """
    Delete a prescription (owner or admin only)
    """
    prescription = db.query(Prescription).filter(Prescription.id == prescription_id).first()
    if not prescription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prescription not found"
        )
    
    # Check if user owns the prescription or is admin
    if prescription.user_id != current_user.id:
        # TODO: Add role-based access control for admin users
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    db.delete(prescription)
    db.commit()
    
    return {"message": "Prescription deleted successfully"}


@router.get("/stats/overview", response_model=PrescriptionStats)
def get_prescription_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> PrescriptionStats:
    """
    Get prescription statistics (admin/pharmacist only)
    """
    # TODO: Add role-based access control for admin/pharmacist users
    
    # Get counts by status
    stats = db.query(
        func.count(Prescription.id).label('total'),
        func.sum(func.case((Prescription.status == PrescriptionStatus.PENDING, 1), else_=0)).label('pending'),
        func.sum(func.case((Prescription.status == PrescriptionStatus.VERIFIED, 1), else_=0)).label('verified'),
        func.sum(func.case((Prescription.status == PrescriptionStatus.REJECTED, 1), else_=0)).label('rejected'),
        func.sum(func.case((Prescription.status == PrescriptionStatus.EXPIRED, 1), else_=0)).label('expired')
    ).first()
    
    return PrescriptionStats(
        total_prescriptions=stats.total or 0,
        pending_verification=stats.pending or 0,
        verified_prescriptions=stats.verified or 0,
        rejected_prescriptions=stats.rejected or 0,
        expired_prescriptions=stats.expired or 0
    )
