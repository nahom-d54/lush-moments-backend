from datetime import datetime
from enum import Enum
from typing import List, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class CategoryEnum(Enum):
    baby_showers = "Baby Showers"
    birthdays = "Birthdays"
    engagements = "Engagements"


class GalleryItemBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: Literal["Baby Showers", "Birthdays", "Engagements"]
    tags: Optional[List[str]] = None  # JSON array of tags
    display_order: int = 0
    is_featured: bool = False


class GalleryItemCreate(BaseModel):
    """Schema for creating gallery item with file upload."""

    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    category: Literal["Baby Showers", "Birthdays", "Engagements"]
    tags: Optional[List[str]] = Field(None, description="List of tags")
    display_order: int = Field(0, ge=0)
    is_featured: bool = False

    class Config:
        # This allows the schema to work with form data
        arbitrary_types_allowed = True


class GalleryItemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    display_order: Optional[int] = None
    is_featured: Optional[bool] = None
    image_url: Optional[str] = None
    thumbnail_url: Optional[str] = None


class GalleryItem(GalleryItemBase):
    id: UUID
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
