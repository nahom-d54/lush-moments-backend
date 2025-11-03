from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class ThemeBase(BaseModel):
    name: str
    description: Optional[str] = None
    category_id: Optional[UUID] = None
    gallery_images: Optional[list[str]] = None
    featured: bool


class ThemeCreate(ThemeBase):
    pass


class ThemeUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[UUID] = None
    gallery_images: Optional[list[str]] = None
    featured: Optional[bool] = None


class Theme(ThemeBase):
    id: UUID
    category_name: Optional[str] = None  # Will be populated from relationship

    class Config:
        from_attributes = True
