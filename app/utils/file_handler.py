"""File upload and storage utilities"""
import os
import uuid
import shutil
from pathlib import Path
from typing import Tuple
from fastapi import UploadFile, HTTPException
from app.config import settings

# Allowed file types
ALLOWED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg", ".tiff", ".tif"}
ALLOWED_MIME_TYPES = {
    "application/pdf",
    "image/png",
    "image/jpeg",
    "image/tiff"
}


def validate_file(file: UploadFile) -> None:
    """
    Validate uploaded file type and size.
    
    Args:
        file: Uploaded file object
        
    Raises:
        HTTPException: If file is invalid
    """
    # Check file extension
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Supported: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Check MIME type
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Got: {file.content_type}"
        )


async def save_upload_file(file: UploadFile, user_id: str) -> Tuple[str, str, int]:
    """
    Save uploaded file to storage directory.
    
    Args:
        file: Uploaded file object
        user_id: ID of the user uploading the file
        
    Returns:
        Tuple of (file_path, filename, file_size)
    """
    # Create user storage directory
    user_storage_dir = Path(settings.STORAGE_DIR) / user_id
    user_storage_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate unique filename
    file_ext = Path(file.filename).suffix.lower()
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = user_storage_dir / unique_filename
    
    # Save file
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    finally:
        file.file.close()
    
    # Get file size
    file_size = file_path.stat().st_size
    
    return str(file_path), unique_filename, file_size


def delete_file(file_path: str) -> None:
    """
    Delete a file from storage.
    
    Args:
        file_path: Path to file to delete
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        # Log error but don't raise - file deletion is not critical
        print(f"Error deleting file {file_path}: {e}")


def get_file_path(user_id: str, filename: str) -> Path:
    """
    Get full path to a stored file.
    
    Args:
        user_id: User ID
        filename: Filename
        
    Returns:
        Full path to file
    """
    return Path(settings.STORAGE_DIR) / user_id / filename

