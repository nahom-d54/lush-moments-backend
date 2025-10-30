from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class ThemeBase(BaseModel):
    name: str
    description: Optional[str] = None
    gallery_images: Optional[list[str]] = None
    featured: bool


class ThemeCreate(ThemeBase):
    pass


class Theme(ThemeBase):
    id: UUID

    class Config:
        from_attributes = True
