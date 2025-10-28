from typing import Optional

from pydantic import BaseModel


class ThemeBase(BaseModel):
    name: str
    description: Optional[str] = None
    gallery_images: Optional[list[str]] = None
    featured: bool


class ThemeCreate(ThemeBase):
    pass


class Theme(ThemeBase):
    id: int

    class Config:
        from_attributes = True
