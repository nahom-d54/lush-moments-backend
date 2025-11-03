import json
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models.gallery_category import GalleryCategory
from app.models.gallery_item import GalleryItem
from app.schemas.gallery_category import (
    GalleryCategory as GalleryCategorySchema,
)
from app.schemas.gallery_category import (
    GalleryCategoryCreate,
    GalleryCategoryUpdate,
)
from app.schemas.gallery_item import GalleryItem as GalleryItemSchema
from app.utils.auth import get_current_admin
from app.utils.image_processing import delete_gallery_image, save_gallery_image

router = APIRouter(prefix="/admin/gallery", tags=["Gallery"])


@router.post("/", response_model=List[GalleryItemSchema], status_code=201)
async def create_gallery_items(
    files: List[UploadFile] = File(..., description="Upload 1-5 images"),
    title: str = Form(...),
    category_id: str = Form(...),  # UUID as string
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

    # Validate category exists
    try:
        cat_uuid = UUID(category_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid category ID format")

    cat_result = await db.execute(
        select(GalleryCategory).where(GalleryCategory.id == cat_uuid)
    )
    category = cat_result.scalar_one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

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
                category_id=cat_uuid,
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

        # Refresh all items with category relationship
        for item in created_items:
            await db.refresh(item)
            # Load category relationship
            await db.execute(
                select(GalleryItem)
                .options(selectinload(GalleryItem.category_obj))
                .where(GalleryItem.id == item.id)
            )

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
    item_id: UUID,
    title: str | None = Form(None),
    category_id: str | None = Form(None),  # UUID as string
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
        # Validate category if provided
        if category_id is not None:
            try:
                cat_uuid = UUID(category_id)
            except ValueError:
                raise HTTPException(
                    status_code=400, detail="Invalid category ID format"
                )

            cat_result = await db.execute(
                select(GalleryCategory).where(GalleryCategory.id == cat_uuid)
            )
            category = cat_result.scalar_one_or_none()
            if not category:
                raise HTTPException(status_code=404, detail="Category not found")
            item.category_id = cat_uuid

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
    item_id: UUID,
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


# Category Management Endpoints


@router.post("/categories", response_model=GalleryCategorySchema, status_code=201)
async def create_category(
    category: GalleryCategoryCreate,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    """Admin endpoint: Create a new gallery category"""
    # Check if slug already exists
    result = await db.execute(
        select(GalleryCategory).where(GalleryCategory.slug == category.slug)
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=400, detail="Category with this slug already exists"
        )

    db_category = GalleryCategory(**category.model_dump())
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category


@router.patch("/categories/{category_id}", response_model=GalleryCategorySchema)
async def update_category(
    category_id: UUID,
    category_update: GalleryCategoryUpdate,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    """Admin endpoint: Update a gallery category"""
    result = await db.execute(
        select(GalleryCategory).where(GalleryCategory.id == category_id)
    )
    category = result.scalar_one_or_none()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    # Check if new slug conflicts
    if category_update.slug and category_update.slug != category.slug:
        slug_result = await db.execute(
            select(GalleryCategory).where(GalleryCategory.slug == category_update.slug)
        )
        if slug_result.scalar_one_or_none():
            raise HTTPException(
                status_code=400, detail="Category with this slug already exists"
            )

    # Update fields
    update_data = category_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(category, field, value)

    await db.commit()
    await db.refresh(category)
    return category


@router.delete("/categories/{category_id}")
async def delete_category(
    category_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    """
    Admin endpoint: Delete a gallery category.
    Note: This will fail if there are gallery items using this category (foreign key constraint).
    """
    result = await db.execute(
        select(GalleryCategory).where(GalleryCategory.id == category_id)
    )
    category = result.scalar_one_or_none()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    # Check if category has items
    items_result = await db.execute(
        select(GalleryItem).where(GalleryItem.category_id == category_id)
    )
    if items_result.scalar_one_or_none():
        raise HTTPException(
            status_code=400,
            detail="Cannot delete category with existing gallery items. Delete or reassign items first.",
        )

    await db.delete(category)
    await db.commit()
    return {"message": "Category deleted successfully"}
