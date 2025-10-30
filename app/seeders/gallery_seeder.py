"""
Gallery Seeder

Seeds gallery items.
"""

from sqlalchemy import select

from app.models import GalleryItem

from .base import BaseSeeder
from .registry import registry


class GallerySeeder(BaseSeeder):
    """Seed gallery items"""

    name = "gallery"
    description = "Create gallery items"
    dependencies = []

    async def should_run(self) -> bool:
        """Check if gallery items already exist"""
        result = await self.db.execute(select(GalleryItem).limit(1))
        return result.first() is None

    async def run(self) -> None:
        """Create gallery items"""
        gallery_items = [
            GalleryItem(
                title="Elegant Wedding Reception",
                description="Beautiful wedding setup with romantic lighting and floral arrangements",
                image_url="/uploads/gallery/wedding_reception_1.jpg",
                thumbnail_url="/uploads/gallery/thumbs/wedding_reception_1_thumb.jpg",
                category="wedding",
                tags=["wedding", "elegant", "romantic", "indoor"],
                is_featured=True,
                display_order=1,
            ),
            GalleryItem(
                title="Corporate Gala Event",
                description="Professional corporate event with modern setup",
                image_url="/uploads/gallery/corporate_gala_1.jpg",
                thumbnail_url="/uploads/gallery/thumbs/corporate_gala_1_thumb.jpg",
                category="corporate",
                tags=["corporate", "professional", "modern"],
                is_featured=True,
                display_order=2,
            ),
            GalleryItem(
                title="Birthday Party Celebration",
                description="Colorful and vibrant birthday party setup",
                image_url="/uploads/gallery/birthday_party_1.jpg",
                thumbnail_url="/uploads/gallery/thumbs/birthday_party_1_thumb.jpg",
                category="birthday",
                tags=["birthday", "colorful", "fun", "outdoor"],
                is_featured=False,
                display_order=3,
            ),
            GalleryItem(
                title="Garden Wedding Ceremony",
                description="Outdoor garden wedding with natural beauty",
                image_url="/uploads/gallery/garden_wedding_1.jpg",
                thumbnail_url="/uploads/gallery/thumbs/garden_wedding_1_thumb.jpg",
                category="wedding",
                tags=["wedding", "outdoor", "garden", "natural"],
                is_featured=True,
                display_order=4,
            ),
            GalleryItem(
                title="Anniversary Dinner Setup",
                description="Intimate anniversary celebration with elegant table settings",
                image_url="/uploads/gallery/anniversary_dinner_1.jpg",
                thumbnail_url="/uploads/gallery/thumbs/anniversary_dinner_1_thumb.jpg",
                category="anniversary",
                tags=["anniversary", "intimate", "elegant"],
                is_featured=False,
                display_order=5,
            ),
        ]
        self.db.add_all(gallery_items)
        await self.db.commit()
        print(f"  - Created {len(gallery_items)} gallery items")


# Auto-register this seeder
registry.register(GallerySeeder)
