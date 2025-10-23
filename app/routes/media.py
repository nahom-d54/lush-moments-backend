import os
import uuid
from pathlib import Path
from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse

from app.utils.auth import get_current_admin

router = APIRouter(prefix="/media", tags=["media"])

# Create uploads directory
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB


def is_allowed_file(filename: str) -> bool:
    """Check if file extension is allowed"""
    return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS


@router.post("/upload", dependencies=[Depends(get_current_admin)])
async def upload_file(file: UploadFile = File(...)):
    """Upload a media file (admin only)"""

    # Check file extension
    if not is_allowed_file(file.filename):
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}",
        )

    # Check file size
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size: {MAX_FILE_SIZE / (1024 * 1024)}MB",
        )

    # Generate unique filename
    file_extension = Path(file.filename).suffix
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = UPLOAD_DIR / unique_filename

    # Save file
    with open(file_path, "wb") as f:
        f.write(contents)

    # Return file URL
    return {
        "filename": unique_filename,
        "url": f"/media/files/{unique_filename}",
        "size": len(contents),
    }


@router.post("/upload-multiple", dependencies=[Depends(get_current_admin)])
async def upload_multiple_files(files: List[UploadFile] = File(...)):
    """Upload multiple media files (admin only)"""

    uploaded_files = []

    for file in files:
        # Check file extension
        if not is_allowed_file(file.filename):
            continue

        # Check file size
        contents = await file.read()
        if len(contents) > MAX_FILE_SIZE:
            continue

        # Generate unique filename
        file_extension = Path(file.filename).suffix
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = UPLOAD_DIR / unique_filename

        # Save file
        with open(file_path, "wb") as f:
            f.write(contents)

        uploaded_files.append(
            {
                "filename": unique_filename,
                "url": f"/media/files/{unique_filename}",
                "size": len(contents),
            }
        )

    return {"files": uploaded_files, "count": len(uploaded_files)}


@router.get("/files/{filename}")
async def get_file(filename: str):
    """Get a media file"""
    file_path = UPLOAD_DIR / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(file_path)


@router.delete("/files/{filename}", dependencies=[Depends(get_current_admin)])
async def delete_file(filename: str):
    """Delete a media file (admin only)"""
    file_path = UPLOAD_DIR / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    os.remove(file_path)
    return {"message": "File deleted successfully"}
