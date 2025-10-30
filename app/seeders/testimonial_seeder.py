"""
Testimonial Seeder

Seeds customer testimonials.
"""

from sqlalchemy import select

from app.models import Testimonial

from .base import BaseSeeder
from .registry import registry


class TestimonialSeeder(BaseSeeder):
    """Seed customer testimonials"""

    name = "testimonials"
    description = "Create customer testimonials"
    dependencies = []

    async def should_run(self) -> bool:
        """Check if testimonials already exist"""
        result = await self.db.execute(select(Testimonial).limit(1))
        return result.first() is None

    async def run(self) -> None:
        """Create testimonials"""
        testimonials = [
            Testimonial(
                name="Sarah Johnson",
                message="Lush Moments made our wedding day absolutely perfect! The attention to detail was incredible, and our guests couldn't stop raving about the venue and food.",
                image_url="/uploads/testimonials/sarah_johnson.jpg",
                rating=5.0,
            ),
            Testimonial(
                name="Michael Chen",
                message="Outstanding service from start to finish. Our corporate event was a huge success thanks to the professional team at Lush Moments. Highly recommended!",
                image_url="/uploads/testimonials/michael_chen.jpg",
                rating=5.0,
            ),
            Testimonial(
                name="Emily Rodriguez",
                message="Beautiful venue, amazing food, and professional staff. Couldn't have asked for more for our daughter's quinceañera!",
                image_url="/uploads/testimonials/emily_rodriguez.jpg",
                rating=4.8,
            ),
            Testimonial(
                name="David Thompson",
                message="The team went above and beyond to make our anniversary celebration special. Every detail was perfect!",
                image_url="/uploads/testimonials/david_thompson.jpg",
                rating=5.0,
            ),
            Testimonial(
                name="Lisa Anderson",
                message="Professional, reliable, and creative. Lush Moments transformed our vision into reality for our company's gala event.",
                image_url="/uploads/testimonials/lisa_anderson.jpg",
                rating=4.9,
            ),
        ]
        self.db.add_all(testimonials)
        await self.db.commit()
        print(f"  - Created {len(testimonials)} testimonials")


# Auto-register this seeder
registry.register(TestimonialSeeder)
