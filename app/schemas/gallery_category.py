from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class GalleryCategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    slug: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    display_order: int = Field(0, ge=0)
    is_active: bool = True


class GalleryCategoryCreate(GalleryCategoryBase):
    pass


class GalleryCategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    slug: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    display_order: Optional[int] = Field(None, ge=0)
    is_active: Optional[bool] = None


class GalleryCategory(GalleryCategoryBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
