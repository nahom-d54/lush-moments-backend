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


@router.post("/", response_model=GalleryItemSchema, status_code=201)
@router.post("", response_model=GalleryItemSchema, status_code=201)
async def create_gallery_item(
    files: List[UploadFile] = File(..., description="Upload 1-10 images"),
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
    Admin endpoint: Create a single gallery item with multiple images (1-10 images).
    The first image becomes the primary image_url, and all images are stored in gallery_images array.
    Each image automatically generates an optimized thumbnail using Pillow.
    """
    # Validate number of files
    if not files or len(files) == 0:
        raise HTTPException(status_code=400, detail="At least one image is required")

    if len(files) > 10:
        raise HTTPException(
            status_code=400, detail="Maximum 10 images allowed per gallery item"
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

    uploaded_images = []
    primary_image_url = None
    primary_thumbnail_url = None

    try:
        # Upload all images
        for idx, file in enumerate(files):
            image_url, thumbnail_url = await save_gallery_image(file)
            uploaded_images.append(image_url)

            # First image is the primary/cover image
            if idx == 0:
                primary_image_url = image_url
                primary_thumbnail_url = thumbnail_url

        # Create single database entry with all images
        db_item = GalleryItem(
            title=title,
            description=description,
            category_id=cat_uuid,
            tags=parsed_tags,
            display_order=display_order,
            is_featured=is_featured,
            image_url=primary_image_url,
            thumbnail_url=primary_thumbnail_url,
            gallery_images=uploaded_images,  # Store all image URLs including primary
        )

        db.add(db_item)
        await db.commit()
        await db.refresh(db_item)

        # Load category relationship
        result = await db.execute(
            select(GalleryItem)
            .options(selectinload(GalleryItem.category_obj))
            .where(GalleryItem.id == db_item.id)
        )
        item = result.scalar_one()

        return item

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
        raise HTTPException(
            status_code=500, detail=f"Failed to create gallery item: {str(e)}"
        )


@router.patch("/{item_id}", response_model=GalleryItemSchema)
@router.patch("/{item_id}/", response_model=GalleryItemSchema)
async def update_gallery_item(
    item_id: UUID,
    title: str | None = Form(None),
    category_id: str | None = Form(None),  # UUID as string
    description: str | None = Form(None),
    tags: str | None = Form(None),
    display_order: int | None = Form(None),
    is_featured: bool | None = Form(None),
    files: List[UploadFile] | None = File(
        None, description="Upload new images (optional, replaces all)"
    ),
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    """
    Admin endpoint: Update a gallery item.
    Optionally upload new images (will replace all existing images).
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

        # If new files are uploaded, replace all images
        if files and len(files) > 0:
            if len(files) > 10:
                raise HTTPException(
                    status_code=400, detail="Maximum 10 images allowed per gallery item"
                )

            # Store old images for cleanup
            old_image_url = item.image_url
            old_thumbnail_url = item.thumbnail_url
            old_gallery_images = item.gallery_images or []

            # Upload new images
            uploaded_images = []
            primary_image_url = None
            primary_thumbnail_url = None

            for idx, file in enumerate(files):
                image_url, thumbnail_url = await save_gallery_image(file)
                uploaded_images.append(image_url)

                if idx == 0:
                    primary_image_url = image_url
                    primary_thumbnail_url = thumbnail_url

            # Update image fields
            item.image_url = primary_image_url
            item.thumbnail_url = primary_thumbnail_url
            item.gallery_images = uploaded_images

            # Delete old images after successful upload
            try:
                delete_gallery_image(old_image_url, old_thumbnail_url)
            except Exception as e:
                print(f"Warning: Failed to delete old primary image: {e}")

            # Delete old gallery images
            for old_img in old_gallery_images:
                if old_img != old_image_url:  # Don't try to delete primary twice
                    try:
                        delete_gallery_image(old_img, None)
                    except Exception as e:
                        print(
                            f"Warning: Failed to delete old gallery image {old_img}: {e}"
                        )

        # Update other fields
        if title is not None:
            item.title = title
        if description is not None:
            item.description = description
        if parsed_tags is not None:
            item.tags = parsed_tags
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
@router.delete("/{item_id}/")
async def delete_gallery_item(
    item_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    """
    Admin endpoint: Delete a gallery item.
    Also deletes associated image files from filesystem (including all gallery images).
    """
    result = await db.execute(select(GalleryItem).where(GalleryItem.id == item_id))
    item = result.scalar_one_or_none()

    if not item:
        raise HTTPException(status_code=404, detail="Gallery item not found")

    # Delete primary images from filesystem
    try:
        delete_gallery_image(item.image_url, item.thumbnail_url)
    except Exception as e:
        print(f"Warning: Failed to delete primary image files: {e}")

    # Delete all gallery images from filesystem
    if item.gallery_images:
        for img_url in item.gallery_images:
            if img_url != item.image_url:  # Don't try to delete primary twice
                try:
                    delete_gallery_image(img_url, None)
                except Exception as e:
                    print(f"Warning: Failed to delete gallery image {img_url}: {e}")

    # Delete from database
    await db.delete(item)
    await db.commit()

    return {"message": "Gallery item deleted successfully"}


# Category Management Endpoints


@router.post("/categories", response_model=GalleryCategorySchema, status_code=201)
@router.post("/categories/", response_model=GalleryCategorySchema, status_code=201)
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
@router.patch("/categories/{category_id}/", response_model=GalleryCategorySchema)
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
@router.delete("/categories/{category_id}/")
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
