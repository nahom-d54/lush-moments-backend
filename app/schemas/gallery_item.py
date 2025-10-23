from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class GalleryItemBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: str
    tags: Optional[str] = None  # JSON string array
    display_order: int = 0
    is_featured: bool = False


class GalleryItemCreate(GalleryItemBase):
    image_url: str
    thumbnail_url: Optional[str] = None


class GalleryItemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[str] = None
    display_order: Optional[int] = None
    is_featured: Optional[bool] = None
    image_url: Optional[str] = None
    thumbnail_url: Optional[str] = None


class GalleryItem(GalleryItemBase):
    id: int
    image_url: str
    thumbnail_url: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class GalleryItemList(BaseModel):
    """Response for gallery list with optional filters"""

    items: List[GalleryItem]
    total: int
    category: Optional[str] = None
