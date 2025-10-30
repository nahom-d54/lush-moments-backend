from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class TestimonialBase(BaseModel):
    name: str
    message: str
    image_url: Optional[str] = None
    rating: float


class TestimonialCreate(TestimonialBase):
    pass


class Testimonial(TestimonialBase):
    id: UUID

    class Config:
        from_attributes = True
