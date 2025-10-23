from typing import Optional

from pydantic import BaseModel


class TestimonialBase(BaseModel):
    name: str
    message: str
    image_url: Optional[str] = None
    rating: float


class TestimonialCreate(TestimonialBase):
    pass


class Testimonial(TestimonialBase):
    id: int

    class Config:
        from_attributes = True
