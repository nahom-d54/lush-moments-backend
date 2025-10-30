"""
Package Enhancement Seeder

Seeds package add-ons and enhancements.
"""

from sqlalchemy import select

from app.models import PackageEnhancement

from .base import BaseSeeder
from .registry import registry


class EnhancementSeeder(BaseSeeder):
    """Seed package enhancements"""

    name = "enhancements"
    description = "Create package add-ons and enhancements"
    dependencies = []

    async def should_run(self) -> bool:
        """Check if enhancements already exist"""
        result = await self.db.execute(select(PackageEnhancement).limit(1))
        return result.first() is None

    async def run(self) -> None:
        """Create enhancements"""
        enhancements_data = [
            {
                "name": "Floral Arrangements",
                "description": "Fresh or silk floral centerpieces and accents",
                "starting_price": 150.0,
                "category": "floral",
                "icon": "🌸",
                "display_order": 1,
            },
            {
                "name": "Photo Booth Setup",
                "description": "Custom backdrop with props and signage",
                "starting_price": 300.0,
                "category": "entertainment",
                "icon": "📸",
                "display_order": 2,
            },
            {
                "name": "Lighting Design",
                "description": "Ambient uplighting and string lights",
                "starting_price": 200.0,
                "category": "decor",
                "icon": "💡",
                "display_order": 3,
            },
            {
                "name": "Dessert Table Styling",
                "description": "Complete dessert display with décor",
                "starting_price": 250.0,
                "category": "food",
                "icon": "🍰",
                "display_order": 4,
            },
            {
                "name": "Lounge Area",
                "description": "Comfortable seating area with décor",
                "starting_price": 400.0,
                "category": "furniture",
                "icon": "🛋️",
                "display_order": 5,
            },
            {
                "name": "Custom Signage",
                "description": "Personalized welcome and directional signs",
                "starting_price": 100.0,
                "category": "decor",
                "icon": "🪧",
                "display_order": 6,
            },
            {
                "name": "Balloon Installations",
                "description": "Custom balloon arches and garlands",
                "starting_price": 180.0,
                "category": "decor",
                "icon": "🎈",
                "display_order": 7,
            },
            {
                "name": "DJ Services",
                "description": "Professional DJ with sound system",
                "starting_price": 500.0,
                "category": "entertainment",
                "icon": "🎵",
                "display_order": 8,
            },
        ]

        for enhancement_data in enhancements_data:
            enhancement = PackageEnhancement(**enhancement_data)
            self.db.add(enhancement)

        await self.db.commit()
        print(f"  - Created {len(enhancements_data)} package enhancements")


# Auto-register this seeder
registry.register(EnhancementSeeder)
