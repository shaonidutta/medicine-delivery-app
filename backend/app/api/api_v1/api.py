"""
Main API router for v1
"""

from fastapi import APIRouter
from app.api.api_v1.endpoints import auth, categories, medicines, prescriptions

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(categories.router, prefix="/categories", tags=["categories"])
api_router.include_router(medicines.router, prefix="/medicines", tags=["medicines"])
api_router.include_router(prescriptions.router, prefix="/prescriptions", tags=["prescriptions"])

# Health check endpoint
@api_router.get("/health")
async def health_check():
    """API health check"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "api": "v1"
    }
