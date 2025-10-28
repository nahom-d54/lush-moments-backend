"""Image processing utilities for uploads and thumbnail generation."""

import uuid
from pathlib import Path
from typing import Tuple

from fastapi import UploadFile
from PIL import Image

# Configuration
UPLOAD_DIR = Path("uploads")
GALLERY_DIR = UPLOAD_DIR / "gallery"
THUMBNAIL_DIR = GALLERY_DIR / "thumbnails"
MAX_IMAGE_SIZE = (2048, 2048)  # Max dimensions for full images
THUMBNAIL_SIZE = (400, 400)  # Thumbnail dimensions
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


def ensure_upload_directories():
    """Create upload directories if they don't exist."""
    GALLERY_DIR.mkdir(parents=True, exist_ok=True)
    THUMBNAIL_DIR.mkdir(parents=True, exist_ok=True)


def validate_image_file(file: UploadFile) -> None:
    """Validate uploaded image file."""
    # Check file extension
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Invalid file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}")

    # Check content type
    if not file.content_type or not file.content_type.startswith("image/"):
        raise ValueError("File must be an image")


async def save_gallery_image(file: UploadFile) -> Tuple[str, str]:
    """
    Save uploaded gallery image and generate thumbnail.

    Args:
        file: Uploaded image file

    Returns:
        Tuple of (image_url, thumbnail_url)

    Raises:
        ValueError: If file validation fails
    """
    # Validate file
    validate_image_file(file)

    # Ensure directories exist
    ensure_upload_directories()

    # Generate unique filename
    file_ext = Path(file.filename).suffix.lower()
    unique_filename = f"{uuid.uuid4()}{file_ext}"

    # Full image path
    image_path = GALLERY_DIR / unique_filename
    thumbnail_path = THUMBNAIL_DIR / unique_filename

    # Read file content
    contents = await file.read()

    # Check file size
    if len(contents) > MAX_FILE_SIZE:
        raise ValueError(
            f"File too large. Maximum size: {MAX_FILE_SIZE // 1024 // 1024}MB"
        )

    # Open and process image
    try:
        with Image.open(file.file) as img:
            # Convert RGBA to RGB if necessary (for JPEG compatibility)
            if img.mode in ("RGBA", "LA", "P"):
                background = Image.new("RGB", img.size, (255, 255, 255))
                if img.mode == "P":
                    img = img.convert("RGBA")
                background.paste(
                    img, mask=img.split()[-1] if img.mode == "RGBA" else None
                )
                img = background

            # Resize main image if too large (maintain aspect ratio)
            img.thumbnail(MAX_IMAGE_SIZE, Image.Resampling.LANCZOS)

            # Save optimized main image
            save_kwargs = {
                "optimize": True,
                "quality": 85,
            }
            if file_ext in [".jpg", ".jpeg"]:
                save_kwargs["progressive"] = True

            img.save(image_path, **save_kwargs)

            # Create and save thumbnail
            img_thumb = img.copy()
            img_thumb.thumbnail(THUMBNAIL_SIZE, Image.Resampling.LANCZOS)
            img_thumb.save(thumbnail_path, **save_kwargs)

    except Exception as e:
        # Clean up any created files on error
        if image_path.exists():
            image_path.unlink()
        if thumbnail_path.exists():
            thumbnail_path.unlink()
        raise ValueError(f"Failed to process image: {str(e)}")

    # Return URLs (relative to uploads directory)
    image_url = f"/uploads/gallery/{unique_filename}"
    thumbnail_url = f"/uploads/gallery/thumbnails/{unique_filename}"

    return image_url, thumbnail_url


def delete_gallery_image(image_url: str, thumbnail_url: str | None = None) -> None:
    """
    Delete gallery image and its thumbnail from filesystem.

    Args:
        image_url: URL of the main image
        thumbnail_url: URL of the thumbnail (optional)
    """
    # Extract filename from URL
    if image_url.startswith("/uploads/gallery/"):
        filename = image_url.split("/")[-1]
        image_path = GALLERY_DIR / filename

        if image_path.exists():
            image_path.unlink()

    # Delete thumbnail
    if thumbnail_url and thumbnail_url.startswith("/uploads/gallery/thumbnails/"):
        filename = thumbnail_url.split("/")[-1]
        thumb_path = THUMBNAIL_DIR / filename

        if thumb_path.exists():
            thumb_path.unlink()
