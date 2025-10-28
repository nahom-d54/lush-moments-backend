import json
from typing import List, Literal

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.gallery_item import GalleryItem
from app.schemas.gallery_item import GalleryItem as GalleryItemSchema
from app.utils.auth import get_current_admin
from app.utils.image_processing import delete_gallery_image, save_gallery_image

router = APIRouter(prefix="/admin/gallery", tags=["Gallery"])


@router.post("/", response_model=List[GalleryItemSchema], status_code=201)
async def create_gallery_items(
    files: List[UploadFile] = File(..., description="Upload 1-5 images"),
    title: str = Form(...),
    category: Literal["Baby Showers", "Birthdays", "Engagements"] = Form(...),
    description: str | None = Form(None),
    tags: str | None = Form(None),
    display_order: int = Form(0),
    is_featured: bool = Form(False),
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    """
    Admin endpoint: Create gallery items with multiple image uploads (1-5 images).
    Each image automatically generates an optimized thumbnail using Pillow.
    All images will share the same title, category, description, and tags.
    """
    # Validate number of files
    if not files or len(files) == 0:
        raise HTTPException(status_code=400, detail="At least one image is required")

    if len(files) > 5:
        raise HTTPException(
            status_code=400, detail="Maximum 5 images allowed per upload"
        )

    created_items = []

    # Parse tags if provided (sent as JSON string from form)
    parsed_tags = None
    if tags:
        try:
            parsed_tags = json.loads(tags)
            if not isinstance(parsed_tags, list):
                raise HTTPException(
                    status_code=400, detail="Tags must be a JSON array of strings"
                )
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=400, detail="Invalid tags format. Expected JSON array."
            )

    try:
        for idx, file in enumerate(files):
            # Save image and generate thumbnail automatically
            image_url, thumbnail_url = await save_gallery_image(file)

            # Create database entry
            # Adjust display_order for each image
            db_item = GalleryItem(
                title=f"{title} ({idx + 1})" if len(files) > 1 else title,
                description=description,
                category=category,
                tags=parsed_tags,  # Use parsed list instead of string
                display_order=display_order + idx,
                is_featured=is_featured
                if idx == 0
                else False,  # Only first image featured
                image_url=image_url,
                thumbnail_url=thumbnail_url,
            )

            db.add(db_item)
            created_items.append(db_item)

        await db.commit()

        # Refresh all items
        for item in created_items:
            await db.refresh(item)

        return created_items

    except ValueError as e:
        await db.rollback()
        # Clean up any uploaded files
        for item in created_items:
            try:
                delete_gallery_image(item.image_url, item.thumbnail_url)
            except Exception:
                pass
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        await db.rollback()
        # Clean up any uploaded files
        for item in created_items:
            try:
                delete_gallery_image(item.image_url, item.thumbnail_url)
            except Exception:
                pass
        raise HTTPException(
            status_code=500, detail=f"Failed to create gallery items: {str(e)}"
        )


@router.patch("/{item_id}", response_model=GalleryItemSchema)
async def update_gallery_item(
    item_id: int,
    title: str | None = Form(None),
    category: str | None = Form(None),
    description: str | None = Form(None),
    tags: str | None = Form(None),
    display_order: int | None = Form(None),
    is_featured: bool | None = Form(None),
    file: UploadFile | None = File(None),
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    """
    Admin endpoint: Update a gallery item.
    Optionally upload a new image (will replace old image and regenerate thumbnail).
    """
    result = await db.execute(select(GalleryItem).where(GalleryItem.id == item_id))
    item = result.scalar_one_or_none()

    if not item:
        raise HTTPException(status_code=404, detail="Gallery item not found")

    try:
        # Parse tags if provided
        parsed_tags = None
        if tags is not None:
            try:
                parsed_tags = json.loads(tags)
                if not isinstance(parsed_tags, list):
                    raise HTTPException(
                        status_code=400, detail="Tags must be a JSON array of strings"
                    )
            except json.JSONDecodeError:
                raise HTTPException(
                    status_code=400, detail="Invalid tags format. Expected JSON array."
                )

        # If a new file is uploaded, replace the image
        if file and file.filename:
            # Delete old images
            old_image_url = item.image_url
            old_thumbnail_url = item.thumbnail_url

            # Save new image and generate thumbnail
            image_url, thumbnail_url = await save_gallery_image(file)

            # Update URLs
            item.image_url = image_url
            item.thumbnail_url = thumbnail_url

            # Delete old files after successful upload
            try:
                delete_gallery_image(old_image_url, old_thumbnail_url)
            except Exception as e:
                print(f"Warning: Failed to delete old image files: {e}")

        # Update other fields
        if title is not None:
            item.title = title
        if category is not None:
            item.category = category
        if description is not None:
            item.description = description
        if parsed_tags is not None:
            item.tags = parsed_tags  # Use parsed list
        if display_order is not None:
            item.display_order = display_order
        if is_featured is not None:
            item.is_featured = is_featured

        await db.commit()
        await db.refresh(item)

        return item

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=500, detail=f"Failed to update gallery item: {str(e)}"
        )


@router.delete("/{item_id}")
async def delete_gallery_item(
    item_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    """
    Admin endpoint: Delete a gallery item.
    Also deletes associated image files from filesystem.
    """
    result = await db.execute(select(GalleryItem).where(GalleryItem.id == item_id))
    item = result.scalar_one_or_none()

    if not item:
        raise HTTPException(status_code=404, detail="Gallery item not found")

    # Delete images from filesystem
    try:
        delete_gallery_image(item.image_url, item.thumbnail_url)
    except Exception as e:
        # Log error but continue with database deletion
        print(f"Warning: Failed to delete image files: {e}")

    # Delete from database
    await db.delete(item)
    await db.commit()

    return {"message": "Gallery item deleted successfully"}
