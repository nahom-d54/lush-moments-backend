from typing import List

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Theme
from app.schemas.theme import Theme as ThemeSchema
from app.utils.auth import get_current_admin
from app.utils.image_processing import delete_gallery_image, save_gallery_image

router = APIRouter(prefix="/admin/themes", tags=["Themes"])


@router.get("/", response_model=List[ThemeSchema])
async def get_themes(
    db: AsyncSession = Depends(get_db), current_admin=Depends(get_current_admin)
):
    result = await db.execute(select(Theme))
    themes = result.scalars().all()
    return themes


@router.post("/", response_model=ThemeSchema)
async def create_theme(
    files: List[UploadFile] = File(..., description="Upload 1-10 theme images"),
    name: str = Form(...),
    description: str | None = Form(None),
    featured: bool = Form(False),
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    """
    Admin endpoint: Create a theme with multiple image uploads (1-10 images).
    Each image automatically generates an optimized thumbnail using Pillow.
    """
    # Validate number of files
    if not files or len(files) == 0:
        raise HTTPException(status_code=400, detail="At least one image is required")

    if len(files) > 10:
        raise HTTPException(
            status_code=400, detail="Maximum 10 images allowed per theme"
        )

    uploaded_images = []

    try:
        # Upload all images
        for file in files:
            image_url, thumbnail_url = await save_gallery_image(file)
            uploaded_images.append(image_url)

        # Create theme with uploaded image URLs
        db_theme = Theme(
            name=name,
            description=description,
            gallery_images=uploaded_images,
            featured=featured,
        )

        db.add(db_theme)
        await db.commit()
        await db.refresh(db_theme)

        return db_theme

    except ValueError as e:
        await db.rollback()
        # Clean up any uploaded files
        for image_url in uploaded_images:
            try:
                delete_gallery_image(image_url, None)
            except Exception:
                pass
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        await db.rollback()
        # Clean up any uploaded files
        for image_url in uploaded_images:
            try:
                delete_gallery_image(image_url, None)
            except Exception:
                pass
        raise HTTPException(status_code=500, detail=f"Failed to create theme: {str(e)}")


@router.get("/{theme_id}", response_model=ThemeSchema)
async def get_theme(
    theme_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    result = await db.execute(select(Theme).where(Theme.id == theme_id))
    theme = result.scalar_one_or_none()
    if not theme:
        raise HTTPException(status_code=404, detail="Theme not found")
    return theme


@router.put("/{theme_id}", response_model=ThemeSchema)
async def update_theme(
    theme_id: int,
    files: List[UploadFile] | None = File(
        None, description="Upload new images (optional)"
    ),
    name: str | None = Form(None),
    description: str | None = Form(None),
    featured: bool | None = Form(None),
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    """
    Admin endpoint: Update a theme.
    Optionally upload new images (will replace existing images).
    """
    result = await db.execute(select(Theme).where(Theme.id == theme_id))
    db_theme = result.scalar_one_or_none()
    if not db_theme:
        raise HTTPException(status_code=404, detail="Theme not found")

    try:
        # If new files are uploaded, replace old images
        if files and len(files) > 0:
            if len(files) > 10:
                raise HTTPException(
                    status_code=400, detail="Maximum 10 images allowed per theme"
                )

            # Store old images for cleanup
            old_images = db_theme.gallery_images or []

            # Upload new images
            uploaded_images = []
            for file in files:
                image_url, thumbnail_url = await save_gallery_image(file)
                uploaded_images.append(image_url)

            # Update gallery_images
            db_theme.gallery_images = uploaded_images

            # Delete old images after successful upload
            for old_image_url in old_images:
                try:
                    delete_gallery_image(old_image_url, None)
                except Exception as e:
                    print(f"Warning: Failed to delete old image {old_image_url}: {e}")

        # Update other fields
        if name is not None:
            db_theme.name = name
        if description is not None:
            db_theme.description = description
        if featured is not None:
            db_theme.featured = featured

        await db.commit()
        await db.refresh(db_theme)
        return db_theme

    except ValueError as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update theme: {str(e)}")


@router.delete("/{theme_id}")
async def delete_theme(
    theme_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    """
    Admin endpoint: Delete a theme.
    Also deletes associated image files from filesystem.
    """
    result = await db.execute(select(Theme).where(Theme.id == theme_id))
    theme = result.scalar_one_or_none()
    if not theme:
        raise HTTPException(status_code=404, detail="Theme not found")

    # Delete images from filesystem
    if theme.gallery_images:
        for image_url in theme.gallery_images:
            try:
                delete_gallery_image(image_url, None)
            except Exception as e:
                # Log error but continue with database deletion
                print(f"Warning: Failed to delete image file {image_url}: {e}")

    # Delete from database
    await db.delete(theme)
    await db.commit()
    return {"message": "Theme deleted successfully"}
