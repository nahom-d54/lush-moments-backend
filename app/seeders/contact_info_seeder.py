"""
Contact Info Seeder

Seeds business contact information.
"""

import json

from sqlalchemy import select

from app.models import ContactInfo

from .base import BaseSeeder
from .registry import registry


class ContactInfoSeeder(BaseSeeder):
    """Seed business contact information"""

    name = "contact_info"
    description = "Create business contact information"
    dependencies = []

    async def should_run(self) -> bool:
        """Check if contact info already exists"""
        result = await self.db.execute(select(ContactInfo).limit(1))
        return result.first() is None

    async def run(self) -> None:
        """Create contact info"""
        business_hours = json.dumps(
            {
                "monday": "9:00 AM - 6:00 PM",
                "tuesday": "9:00 AM - 6:00 PM",
                "wednesday": "9:00 AM - 6:00 PM",
                "thursday": "9:00 AM - 6:00 PM",
                "friday": "9:00 AM - 8:00 PM",
                "saturday": "10:00 AM - 8:00 PM",
                "sunday": "Closed",
            }
        )

        contact_info = ContactInfo(
            email="info@lushmoments.com",
            phone="+1-555-LUSH-MOMENTS",
            location="123 Event Plaza, Suite 456, Los Angeles, CA 90001",
            business_hours=business_hours,
            secondary_phone="+1-555-EVENT-NOW",
            secondary_email="bookings@lushmoments.com",
            facebook_url="https://facebook.com/lushmoments",
            instagram_url="https://instagram.com/lushmoments",
            twitter_url="https://twitter.com/lushmoments",
            linkedin_url="https://linkedin.com/company/lushmoments",
            google_maps_url="https://maps.google.com/?q=123+Event+Plaza+Los+Angeles",
        )
        self.db.add(contact_info)
        await self.db.commit()
        print("  - Created business contact information")


# Auto-register this seeder
registry.register(ContactInfoSeeder)
