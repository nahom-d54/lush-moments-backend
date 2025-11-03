"""
Gallery Seeder

Seeds gallery items.
"""

from sqlalchemy import select

from app.models import GalleryItem
from app.models.gallery_category import GalleryCategory

from .base import BaseSeeder
from .registry import registry


class GallerySeeder(BaseSeeder):
    """Seed gallery items"""

    name = "gallery"
    description = "Create gallery items"
    dependencies = ["gallery_categories"]  # Must run after categories are created

    async def should_run(self) -> bool:
        """Check if gallery items already exist"""
        result = await self.db.execute(select(GalleryItem).limit(1))
        return result.first() is None

    async def run(self) -> None:
        """Create gallery items"""
        # Get category IDs by slug
        categories = {}
        for slug in ["weddings", "corporate", "birthdays", "anniversaries"]:
            result = await self.db.execute(
                select(GalleryCategory).where(GalleryCategory.slug == slug)
            )
            category = result.scalar_one_or_none()
            if category:
                categories[slug] = category.id

        if not categories:
            print("  - No categories found, skipping gallery items")
            return

        gallery_items = [
            GalleryItem(
                title="Elegant Wedding Reception",
                description="Beautiful wedding setup with romantic lighting and floral arrangements",
                image_url="/uploads/gallery/wedding_reception_1.jpg",
                thumbnail_url="/uploads/gallery/thumbs/wedding_reception_1_thumb.jpg",
                category_id=categories.get("weddings"),
                tags=["wedding", "elegant", "romantic", "indoor"],
                is_featured=True,
                display_order=1,
            ),
            GalleryItem(
                title="Corporate Gala Event",
                description="Professional corporate event with modern setup",
                image_url="/uploads/gallery/corporate_gala_1.jpg",
                thumbnail_url="/uploads/gallery/thumbs/corporate_gala_1_thumb.jpg",
                category_id=categories.get("corporate"),
                tags=["corporate", "professional", "modern"],
                is_featured=True,
                display_order=2,
            ),
            GalleryItem(
                title="Birthday Party Celebration",
                description="Colorful and vibrant birthday party setup",
                image_url="/uploads/gallery/birthday_party_1.jpg",
                thumbnail_url="/uploads/gallery/thumbs/birthday_party_1_thumb.jpg",
                category_id=categories.get("birthdays"),
                tags=["birthday", "colorful", "fun", "outdoor"],
                is_featured=False,
                display_order=3,
            ),
            GalleryItem(
                title="Garden Wedding Ceremony",
                description="Outdoor garden wedding with natural beauty",
                image_url="/uploads/gallery/garden_wedding_1.jpg",
                thumbnail_url="/uploads/gallery/thumbs/garden_wedding_1_thumb.jpg",
                category_id=categories.get("weddings"),
                tags=["wedding", "outdoor", "garden", "natural"],
                is_featured=True,
                display_order=4,
            ),
            GalleryItem(
                title="Anniversary Dinner Setup",
                description="Intimate anniversary celebration with elegant table settings",
                image_url="/uploads/gallery/anniversary_dinner_1.jpg",
                thumbnail_url="/uploads/gallery/thumbs/anniversary_dinner_1_thumb.jpg",
                category_id=categories.get("anniversaries"),
                tags=["anniversary", "intimate", "elegant"],
                is_featured=False,
                display_order=5,
            ),
        ]

        # Only add items that have valid category IDs
        valid_items = [item for item in gallery_items if item.category_id is not None]

        if valid_items:
            self.db.add_all(valid_items)
            await self.db.commit()
            print(f"  - Created {len(valid_items)} gallery items")
        else:
            print("  - No valid gallery items to create")


# Auto-register this seeder
registry.register(GallerySeeder)
