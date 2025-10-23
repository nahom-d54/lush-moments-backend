from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.gallery_item import GalleryItem
from app.schemas.gallery_item import (
    GalleryItem as GalleryItemSchema,
)
from app.schemas.gallery_item import (
    GalleryItemList,
)

router = APIRouter(prefix="/gallery", tags=["Gallery"])


@router.get("/", response_model=GalleryItemList)
async def get_gallery_items(
    category: str = None,
    featured_only: bool = False,
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
):
    """
    Public endpoint: Get gallery items with optional filters.
    Can filter by category and featured status.
    """
    query = select(GalleryItem).offset(skip).limit(limit)
    count_query = select(func.count(GalleryItem.id))

    # Apply filters
    if category:
        query = query.where(GalleryItem.category == category)
        count_query = count_query.where(GalleryItem.category == category)

    if featured_only:
        query = query.where(GalleryItem.is_featured.is_(True))
        count_query = count_query.where(GalleryItem.is_featured.is_(True))

    # Order by display_order, then by created_at descending
    query = query.order_by(GalleryItem.display_order, GalleryItem.created_at.desc())

    # Execute queries
    result = await db.execute(query)
    items = result.scalars().all()

    count_result = await db.execute(count_query)
    total = count_result.scalar()

    return GalleryItemList(items=items, total=total, category=category)


@router.get("/categories")
async def get_gallery_categories(db: AsyncSession = Depends(get_db)):
    """Public endpoint: Get all unique gallery categories"""
    query = select(GalleryItem.category).distinct()
    result = await db.execute(query)
    categories = result.scalars().all()
    return {"categories": categories}


@router.get("/{item_id}", response_model=GalleryItemSchema)
async def get_gallery_item(item_id: int, db: AsyncSession = Depends(get_db)):
    """Public endpoint: Get a specific gallery item"""
    result = await db.execute(select(GalleryItem).where(GalleryItem.id == item_id))
    item = result.scalar_one_or_none()

    if not item:
        raise HTTPException(status_code=404, detail="Gallery item not found")

    return item
