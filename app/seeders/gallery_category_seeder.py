"""
Gallery Category Seeder

Seeds gallery categories for organizing gallery items.
"""

from sqlalchemy import select

from app.models.gallery_category import GalleryCategory

from .base import BaseSeeder
from .registry import registry


class GalleryCategorySeeder(BaseSeeder):
    """Seed gallery categories"""

    name = "gallery_categories"
    description = "Create gallery categories"
    dependencies = []

    async def should_run(self) -> bool:
        """Check if gallery categories already exist"""
        result = await self.db.execute(select(GalleryCategory).limit(1))
        return result.first() is None

    async def run(self) -> None:
        """Create gallery categories"""
        categories = [
            GalleryCategory(
                name="Weddings",
                slug="weddings",
                description="Beautiful wedding celebrations and ceremonies",
                display_order=1,
            ),
            GalleryCategory(
                name="Birthdays",
                slug="birthdays",
                description="Birthday parties and celebrations for all ages",
                display_order=2,
            ),
            GalleryCategory(
                name="Baby Showers",
                slug="baby-showers",
                description="Welcoming new arrivals with style and joy",
                display_order=3,
            ),
            GalleryCategory(
                name="Engagements",
                slug="engagements",
                description="Celebrating love and commitment",
                display_order=4,
            ),
            GalleryCategory(
                name="Corporate Events",
                slug="corporate",
                description="Professional events and corporate gatherings",
                display_order=5,
            ),
            GalleryCategory(
                name="Anniversaries",
                slug="anniversaries",
                description="Milestone celebrations and anniversary parties",
                display_order=6,
            ),
        ]

        self.db.add_all(categories)
        await self.db.commit()
        print(f"  - Created {len(categories)} gallery categories")


# Auto-register this seeder
registry.register(GalleryCategorySeeder)
