from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class GalleryItemBase(BaseModel):
    title: str
    description: Optional[str] = None
    category_id: UUID
    tags: Optional[List[str]] = None  # JSON array of tags
    display_order: int = 0
    is_featured: bool = False


class GalleryItemCreate(BaseModel):
    """Schema for creating gallery item with file upload."""

    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    category_id: UUID
    tags: Optional[List[str]] = Field(None, description="List of tags")
    display_order: int = Field(0, ge=0)
    is_featured: bool = False

    class Config:
        # This allows the schema to work with form data
        arbitrary_types_allowed = True


class GalleryItemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[UUID] = None
    tags: Optional[List[str]] = None
    display_order: Optional[int] = None
    is_featured: Optional[bool] = None
    image_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    gallery_images: Optional[List[str]] = None


class GalleryItem(GalleryItemBase):
    id: UUID
    image_url: str
    thumbnail_url: Optional[str] = None
    gallery_images: Optional[List[str]] = None  # Additional images
    created_at: datetime
    category_name: Optional[str] = None  # Will be populated from relationship

    class Config:
        from_attributes = True


class GalleryItemList(BaseModel):
    """Response for gallery list with optional filters"""

    items: List[GalleryItem]
    total: int
    category: Optional[str] = None
