"""
Package Seeder

Seeds event packages with items.
"""

from sqlalchemy import select

from app.models import Package, PackageItem

from .base import BaseSeeder
from .registry import registry


class PackageSeeder(BaseSeeder):
    """Seed event packages with bullet point items"""

    name = "packages"
    description = "Create event packages with items"
    dependencies = []

    async def should_run(self) -> bool:
        """Check if packages already exist"""
        result = await self.db.execute(select(Package).limit(1))
        return result.first() is None

    async def run(self) -> None:
        """Create packages with items"""
        packages_data = [
            {
                "title": "Starter Package",
                "description": "Perfect for small intimate gatherings and events",
                "price": 500.0,
                "is_popular": False,
                "display_order": 1,
                "items": [
                    "Venue accommodation for up to 50 guests",
                    "Basic catering services with 3 meal options",
                    "Standard decoration package",
                    "4 hours of event time",
                    "Basic sound system",
                ],
            },
            {
                "title": "Classic Package",
                "description": "Ideal for medium-sized events with comprehensive services",
                "price": 1200.0,
                "is_popular": True,
                "display_order": 2,
                "items": [
                    "Venue accommodation for up to 100 guests",
                    "Full catering with 5 meal options and beverages",
                    "Premium decoration package with centerpieces",
                    "Professional photography (4 hours)",
                    "Advanced sound system with wireless microphones",
                    "Dedicated event coordinator",
                    "6 hours of event time",
                ],
            },
            {
                "title": "Premium Package",
                "description": "Complete luxury experience for unforgettable events",
                "price": 2500.0,
                "is_popular": True,
                "display_order": 3,
                "items": [
                    "Venue accommodation for up to 150 guests",
                    "Gourmet catering with customizable menu",
                    "Luxury decoration with floral arrangements",
                    "Professional photography and videography (6 hours)",
                    "Live entertainment (DJ or band)",
                    "Premium lighting and AV equipment",
                    "Dedicated event planning team",
                    "Custom event signage and programs",
                    "8 hours of event time",
                ],
            },
            {
                "title": "Ultimate Package",
                "description": "All-inclusive premium service for grand celebrations",
                "price": 5000.0,
                "is_popular": False,
                "display_order": 4,
                "items": [
                    "Venue accommodation for up to 300 guests",
                    "Premium gourmet catering with chef's special menu",
                    "Designer decoration with custom themes",
                    "Full media coverage (photo & video team)",
                    "Live band performance",
                    "Professional event coordinator and support staff",
                    "Valet parking services",
                    "Custom cake and dessert bar",
                    "Welcome cocktail hour",
                    "Personalized guest favors",
                    "12 hours of event time",
                ],
            },
        ]

        for pkg_data in packages_data:
            items = pkg_data.pop("items")
            package = Package(**pkg_data)
            self.db.add(package)
            await self.db.flush()  # Get package ID

            for idx, item_text in enumerate(items):
                package_item = PackageItem(
                    package_id=package.id, item_text=item_text, display_order=idx
                )
                self.db.add(package_item)

        await self.db.commit()
        print(f"  - Created {len(packages_data)} packages with items")


# Auto-register this seeder
registry.register(PackageSeeder)
