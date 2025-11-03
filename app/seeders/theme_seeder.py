"""
Theme Seeder

Seeds event themes.
"""

from sqlalchemy import select

from app.models import Theme
from app.models.gallery_category import GalleryCategory

from .base import BaseSeeder
from .registry import registry


class ThemeSeeder(BaseSeeder):
    """Seed event themes"""

    name = "themes"
    description = "Create event themes"
    dependencies = ["gallery_categories"]

    async def should_run(self) -> bool:
        """Check if themes already exist"""
        result = await self.db.execute(select(Theme).limit(1))
        return result.first() is None

    async def run(self) -> None:
        """Create themes"""
        # Fetch category IDs by slug
        categories = {}
        for slug in ["weddings", "birthdays", "corporate-events", "anniversaries"]:
            result = await self.db.execute(
                select(GalleryCategory).where(GalleryCategory.slug == slug)
            )
            category = result.scalar_one_or_none()
            if category:
                categories[slug] = category.id

        themes = [
            Theme(
                name="Romantic Garden",
                description="Elegant outdoor setting with floral arrangements and soft lighting",
                category_id=categories.get("weddings"),
                gallery_images=[
                    "/uploads/themes/romantic_garden_1.jpg",
                    "/uploads/themes/romantic_garden_2.jpg",
                    "/uploads/themes/romantic_garden_3.jpg",
                ],
            ),
            Theme(
                name="Modern Minimalist",
                description="Clean lines, contemporary design, and sophisticated aesthetics",
                category_id=categories.get("weddings"),
                gallery_images=[
                    "/uploads/themes/modern_minimal_1.jpg",
                    "/uploads/themes/modern_minimal_2.jpg",
                ],
            ),
            Theme(
                name="Rustic Charm",
                description="Natural wood elements, vintage decor, and warm ambiance",
                category_id=categories.get("weddings"),
                gallery_images=[
                    "/uploads/themes/rustic_charm_1.jpg",
                    "/uploads/themes/rustic_charm_2.jpg",
                    "/uploads/themes/rustic_charm_3.jpg",
                ],
            ),
            Theme(
                name="Classic Elegance",
                description="Timeless sophistication with luxurious details",
                category_id=categories.get("anniversaries"),
                gallery_images=[
                    "/uploads/themes/classic_elegance_1.jpg",
                    "/uploads/themes/classic_elegance_2.jpg",
                ],
            ),
            Theme(
                name="Tropical Paradise",
                description="Vibrant colors, exotic flowers, and island-inspired decor",
                category_id=categories.get("birthdays"),
                gallery_images=[
                    "/uploads/themes/tropical_paradise_1.jpg",
                    "/uploads/themes/tropical_paradise_2.jpg",
                    "/uploads/themes/tropical_paradise_3.jpg",
                ],
            ),
            Theme(
                name="Corporate Professional",
                description="Sleek and professional setup for business events",
                category_id=categories.get("corporate-events"),
                gallery_images=[
                    "/uploads/themes/corporate_prof_1.jpg",
                    "/uploads/themes/corporate_prof_2.jpg",
                ],
            ),
        ]
        self.db.add_all(themes)
        await self.db.commit()
        print(f"  - Created {len(themes)} themes with categories")


# Auto-register this seeder
registry.register(ThemeSeeder)
