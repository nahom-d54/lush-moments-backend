"""
Theme Seeder

Seeds event themes.
"""

from sqlalchemy import select

from app.models import Theme

from .base import BaseSeeder
from .registry import registry


class ThemeSeeder(BaseSeeder):
    """Seed event themes"""

    name = "themes"
    description = "Create event themes"
    dependencies = []

    async def should_run(self) -> bool:
        """Check if themes already exist"""
        result = await self.db.execute(select(Theme).limit(1))
        return result.first() is None

    async def run(self) -> None:
        """Create themes"""
        themes = [
            Theme(
                name="Romantic Garden",
                description="Elegant outdoor setting with floral arrangements and soft lighting",
                gallery_images=[
                    "/uploads/themes/romantic_garden_1.jpg",
                    "/uploads/themes/romantic_garden_2.jpg",
                    "/uploads/themes/romantic_garden_3.jpg",
                ],
            ),
            Theme(
                name="Modern Minimalist",
                description="Clean lines, contemporary design, and sophisticated aesthetics",
                gallery_images=[
                    "/uploads/themes/modern_minimal_1.jpg",
                    "/uploads/themes/modern_minimal_2.jpg",
                ],
            ),
            Theme(
                name="Rustic Charm",
                description="Natural wood elements, vintage decor, and warm ambiance",
                gallery_images=[
                    "/uploads/themes/rustic_charm_1.jpg",
                    "/uploads/themes/rustic_charm_2.jpg",
                    "/uploads/themes/rustic_charm_3.jpg",
                ],
            ),
            Theme(
                name="Classic Elegance",
                description="Timeless sophistication with luxurious details",
                gallery_images=[
                    "/uploads/themes/classic_elegance_1.jpg",
                    "/uploads/themes/classic_elegance_2.jpg",
                ],
            ),
            Theme(
                name="Tropical Paradise",
                description="Vibrant colors, exotic flowers, and island-inspired decor",
                gallery_images=[
                    "/uploads/themes/tropical_paradise_1.jpg",
                    "/uploads/themes/tropical_paradise_2.jpg",
                    "/uploads/themes/tropical_paradise_3.jpg",
                ],
            ),
            Theme(
                name="Corporate Professional",
                description="Sleek and professional setup for business events",
                gallery_images=[
                    "/uploads/themes/corporate_prof_1.jpg",
                    "/uploads/themes/corporate_prof_2.jpg",
                ],
            ),
        ]
        self.db.add_all(themes)
        await self.db.commit()
        print(f"  - Created {len(themes)} themes")


# Auto-register this seeder
registry.register(ThemeSeeder)
