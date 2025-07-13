"""
File upload service for handling prescription images and other files
"""

import os
import uuid
import shutil
from pathlib import Path
from fastapi import UploadFile, HTTPException
from typing import Optional
from app.core.config import settings


class FileUploadService:
    """Service for handling file uploads"""
    
    def __init__(self):
        self.upload_dir = Path("uploads")
        self.upload_dir.mkdir(exist_ok=True)
        
        # Create subdirectories
        self.prescriptions_dir = self.upload_dir / "prescriptions"
        self.prescriptions_dir.mkdir(exist_ok=True)
    
    def upload_file(self, file: UploadFile, folder: str = "general") -> str:
        """
        Upload a file to local storage
        
        Args:
            file: The uploaded file
            folder: Subfolder to store the file in
            
        Returns:
            str: The file URL/path
        """
        try:
            # Generate unique filename
            file_extension = Path(file.filename).suffix if file.filename else ""
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            
            # Create folder path
            folder_path = self.upload_dir / folder
            folder_path.mkdir(exist_ok=True)
            
            # Full file path
            file_path = folder_path / unique_filename
            
            # Save file
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            # Return relative path as URL
            return f"/uploads/{folder}/{unique_filename}"
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to upload file: {str(e)}"
            )
    
    def delete_file(self, file_path: str) -> bool:
        """
        Delete a file from storage
        
        Args:
            file_path: The file path to delete
            
        Returns:
            bool: True if deleted successfully
        """
        try:
            # Remove leading slash and convert to Path
            clean_path = file_path.lstrip("/")
            full_path = Path(clean_path)
            
            if full_path.exists():
                full_path.unlink()
                return True
            return False
            
        except Exception:
            return False
    
    def get_file_info(self, file_path: str) -> Optional[dict]:
        """
        Get file information
        
        Args:
            file_path: The file path
            
        Returns:
            dict: File information or None if not found
        """
        try:
            clean_path = file_path.lstrip("/")
            full_path = Path(clean_path)
            
            if full_path.exists():
                stat = full_path.stat()
                return {
                    "size": stat.st_size,
                    "created": stat.st_ctime,
                    "modified": stat.st_mtime,
                    "exists": True
                }
            return None
            
        except Exception:
            return None


# Global instance
file_service = FileUploadService()


def upload_file(file: UploadFile, folder: str = "general") -> str:
    """
    Upload a file using the global file service
    
    Args:
        file: The uploaded file
        folder: Subfolder to store the file in
        
    Returns:
        str: The file URL/path
    """
    return file_service.upload_file(file, folder)


def delete_file(file_path: str) -> bool:
    """
    Delete a file using the global file service
    
    Args:
        file_path: The file path to delete
        
    Returns:
        bool: True if deleted successfully
    """
    return file_service.delete_file(file_path)


def get_file_info(file_path: str) -> Optional[dict]:
    """
    Get file information using the global file service
    
    Args:
        file_path: The file path
        
    Returns:
        dict: File information or None if not found
    """
    return file_service.get_file_info(file_path)
