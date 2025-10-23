from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.gallery_item import GalleryItem
from app.schemas.gallery_item import (
    GalleryItem as GalleryItemSchema,
)
from app.schemas.gallery_item import (
    GalleryItemCreate,
    GalleryItemUpdate,
)
from app.utils.auth import get_current_admin

router = APIRouter(prefix="/admin/gallery", tags=["Admin - Gallery"])


@router.post("/", response_model=GalleryItemSchema)
async def create_gallery_item(
    item: GalleryItemCreate,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    """Admin endpoint: Create a new gallery item"""
    db_item = GalleryItem(
        title=item.title,
        description=item.description,
        image_url=item.image_url,
        thumbnail_url=item.thumbnail_url,
        category=item.category,
        tags=item.tags,
        display_order=item.display_order,
        is_featured=item.is_featured,
    )
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item


@router.patch("/{item_id}", response_model=GalleryItemSchema)
async def update_gallery_item(
    item_id: int,
    update_data: GalleryItemUpdate,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    """Admin endpoint: Update a gallery item"""
    result = await db.execute(select(GalleryItem).where(GalleryItem.id == item_id))
    item = result.scalar_one_or_none()

    if not item:
        raise HTTPException(status_code=404, detail="Gallery item not found")

    # Update fields
    update_dict = update_data.model_dump(exclude_unset=True)
    for field, value in update_dict.items():
        setattr(item, field, value)

    await db.commit()
    await db.refresh(item)

    return item


@router.delete("/{item_id}")
async def delete_gallery_item(
    item_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    """Admin endpoint: Delete a gallery item"""
    result = await db.execute(select(GalleryItem).where(GalleryItem.id == item_id))
    item = result.scalar_one_or_none()

    if not item:
        raise HTTPException(status_code=404, detail="Gallery item not found")

    await db.delete(item)
    await db.commit()

    return {"message": "Gallery item deleted successfully"}
