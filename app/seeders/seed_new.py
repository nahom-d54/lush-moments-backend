"""
Database Seeder Module - Updated for Professional Models

Provides functions to seed the database with initial data for development and testing.
"""

import asyncio
import json
from datetime import datetime, timedelta

from sqlalchemy import select

from app.database import AsyncSessionLocal, Base, engine
from app.models import (
    ContactInfo,
    ContactMessage,
    EventBooking,
    GalleryItem,
    Package,
    PackageItem,
    Testimonial,
    Theme,
    Translation,
    User,
)
from app.utils.auth import get_password_hash


async def create_tables():
    """Create all database tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✓ Database tables created")


async def clear_tables():
    """Clear all data from tables (use with caution!)"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    print("✓ Database tables cleared and recreated")


async def seed_users():
    """Seed admin and sample users"""
    async with AsyncSessionLocal() as db:
        # Check if admin already exists
        result = await db.execute(
            select(User).where(User.email == "admin@lushmoments.com")
        )
        existing_admin = result.scalar_one_or_none()

        if existing_admin:
            print("⚠ Admin user already exists, skipping...")
            return

        # Create admin user
        admin = User(
            name="Admin User",
            email="admin@lushmoments.com",
            phone="+1234567890",
            password_hash=get_password_hash("Admin@123"),
            role="admin",
        )
        db.add(admin)

        # Create sample client user
        client = User(
            name="John Client",
            email="client@example.com",
            phone="+1987654321",
            password_hash=get_password_hash("Client@123"),
            role="client",
        )
        db.add(client)

        await db.commit()
        print("✓ Users seeded successfully")
        print("  - Admin: admin@lushmoments.com / Admin@123")
        print("  - Client: client@example.com / Client@123")


async def seed_packages():
    """Seed event packages with bullet point items"""
    async with AsyncSessionLocal() as db:
        # Check if packages already exist
        result = await db.execute(select(Package))
        existing_packages = result.scalars().all()

        if existing_packages:
            print("⚠ Packages already exist, skipping...")
            return

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
            db.add(package)
            await db.flush()  # Get package ID

            for idx, item_text in enumerate(items):
                package_item = PackageItem(
                    package_id=package.id, item_text=item_text, display_order=idx
                )
                db.add(package_item)

        await db.commit()
        print(f"✓ {len(packages_data)} packages with items seeded successfully")


async def seed_gallery():
    """Seed gallery items"""
    async with AsyncSessionLocal() as db:
        # Check if gallery items already exist
        result = await db.execute(select(GalleryItem))
        existing_items = result.scalars().all()

        if existing_items:
            print("⚠ Gallery items already exist, skipping...")
            return

        gallery_items = [
            GalleryItem(
                title="Elegant Wedding Reception",
                description="Beautiful wedding setup with romantic lighting and floral arrangements",
                image_url="/uploads/gallery/wedding_reception_1.jpg",
                thumbnail_url="/uploads/gallery/thumbs/wedding_reception_1_thumb.jpg",
                category="wedding",
                tags=json.dumps(["wedding", "elegant", "romantic", "indoor"]),
                is_featured=True,
                display_order=1,
            ),
            GalleryItem(
                title="Corporate Gala Event",
                description="Professional corporate event with modern setup",
                image_url="/uploads/gallery/corporate_gala_1.jpg",
                thumbnail_url="/uploads/gallery/thumbs/corporate_gala_1_thumb.jpg",
                category="corporate",
                tags=json.dumps(["corporate", "professional", "modern"]),
                is_featured=True,
                display_order=2,
            ),
            GalleryItem(
                title="Birthday Party Celebration",
                description="Colorful and vibrant birthday party setup",
                image_url="/uploads/gallery/birthday_party_1.jpg",
                thumbnail_url="/uploads/gallery/thumbs/birthday_party_1_thumb.jpg",
                category="birthday",
                tags=json.dumps(["birthday", "colorful", "fun", "outdoor"]),
                is_featured=False,
                display_order=3,
            ),
            GalleryItem(
                title="Garden Wedding Ceremony",
                description="Outdoor garden wedding with natural beauty",
                image_url="/uploads/gallery/garden_wedding_1.jpg",
                thumbnail_url="/uploads/gallery/thumbs/garden_wedding_1_thumb.jpg",
                category="wedding",
                tags=json.dumps(["wedding", "outdoor", "garden", "natural"]),
                is_featured=True,
                display_order=4,
            ),
            GalleryItem(
                title="Anniversary Dinner Setup",
                description="Intimate anniversary celebration with elegant table settings",
                image_url="/uploads/gallery/anniversary_dinner_1.jpg",
                thumbnail_url="/uploads/gallery/thumbs/anniversary_dinner_1_thumb.jpg",
                category="anniversary",
                tags=json.dumps(["anniversary", "intimate", "elegant"]),
                is_featured=False,
                display_order=5,
            ),
        ]
        db.add_all(gallery_items)
        await db.commit()
        print(f"✓ {len(gallery_items)} gallery items seeded successfully")


async def seed_contact_info():
    """Seed business contact information"""
    async with AsyncSessionLocal() as db:
        # Check if contact info already exists
        result = await db.execute(select(ContactInfo))
        existing_info = result.scalar_one_or_none()

        if existing_info:
            print("⚠ Contact info already exists, skipping...")
            return

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
        db.add(contact_info)
        await db.commit()
        print("✓ Contact information seeded successfully")


async def seed_contact_messages():
    """Seed sample contact form messages"""
    async with AsyncSessionLocal() as db:
        # Check if contact messages already exist
        result = await db.execute(select(ContactMessage))
        existing_messages = result.scalars().all()

        if existing_messages:
            print("⚠ Contact messages already exist, skipping...")
            return

        messages = [
            ContactMessage(
                full_name="Jane Smith",
                email="jane.smith@email.com",
                phone_number="+1-555-0123",
                message="I'm interested in booking your Classic Package for my wedding in June. Can you provide more details about customization options?",
                is_read=False,
                created_at=datetime.utcnow() - timedelta(days=2),
            ),
            ContactMessage(
                full_name="Robert Johnson",
                email="robert.j@company.com",
                phone_number="+1-555-0456",
                message="Looking to organize a corporate event for 200 people. What packages would you recommend?",
                is_read=True,
                created_at=datetime.utcnow() - timedelta(days=5),
                responded_at=datetime.utcnow() - timedelta(days=4),
            ),
        ]
        db.add_all(messages)
        await db.commit()
        print(f"✓ {len(messages)} contact messages seeded successfully")


async def seed_themes():
    """Seed event themes"""
    async with AsyncSessionLocal() as db:
        # Check if themes already exist
        result = await db.execute(select(Theme))
        existing_themes = result.scalars().all()

        if existing_themes:
            print("⚠ Themes already exist, skipping...")
            return

        themes = [
            Theme(
                name="Romantic Garden",
                description="Elegant outdoor setting with floral arrangements and soft lighting",
                gallery_images=json.dumps(
                    [
                        "/uploads/themes/romantic_garden_1.jpg",
                        "/uploads/themes/romantic_garden_2.jpg",
                        "/uploads/themes/romantic_garden_3.jpg",
                    ]
                ),
            ),
            Theme(
                name="Modern Minimalist",
                description="Clean lines, contemporary design, and sophisticated aesthetics",
                gallery_images=json.dumps(
                    [
                        "/uploads/themes/modern_minimal_1.jpg",
                        "/uploads/themes/modern_minimal_2.jpg",
                    ]
                ),
            ),
            Theme(
                name="Rustic Charm",
                description="Natural wood elements, vintage decor, and warm ambiance",
                gallery_images=json.dumps(
                    [
                        "/uploads/themes/rustic_charm_1.jpg",
                        "/uploads/themes/rustic_charm_2.jpg",
                        "/uploads/themes/rustic_charm_3.jpg",
                    ]
                ),
            ),
            Theme(
                name="Classic Elegance",
                description="Timeless sophistication with luxurious details",
                gallery_images=json.dumps(
                    [
                        "/uploads/themes/classic_elegance_1.jpg",
                        "/uploads/themes/classic_elegance_2.jpg",
                    ]
                ),
            ),
            Theme(
                name="Tropical Paradise",
                description="Vibrant colors, exotic flowers, and island-inspired decor",
                gallery_images=json.dumps(
                    [
                        "/uploads/themes/tropical_paradise_1.jpg",
                        "/uploads/themes/tropical_paradise_2.jpg",
                        "/uploads/themes/tropical_paradise_3.jpg",
                    ]
                ),
            ),
            Theme(
                name="Corporate Professional",
                description="Sleek and professional setup for business events",
                gallery_images=json.dumps(
                    [
                        "/uploads/themes/corporate_prof_1.jpg",
                        "/uploads/themes/corporate_prof_2.jpg",
                    ]
                ),
            ),
        ]
        db.add_all(themes)
        await db.commit()
        print(f"✓ {len(themes)} themes seeded successfully")


async def seed_testimonials():
    """Seed customer testimonials"""
    async with AsyncSessionLocal() as db:
        # Check if testimonials already exist
        result = await db.execute(select(Testimonial))
        existing_testimonials = result.scalars().all()

        if existing_testimonials:
            print("⚠ Testimonials already exist, skipping...")
            return

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
        db.add_all(testimonials)
        await db.commit()
        print(f"✓ {len(testimonials)} testimonials seeded successfully")


async def seed_sample_bookings():
    """Seed sample event bookings"""
    async with AsyncSessionLocal() as db:
        # Check if bookings already exist
        result = await db.execute(select(EventBooking))
        existing_bookings = result.scalars().all()

        if existing_bookings:
            print("⚠ Bookings already exist, skipping...")
            return

        # Get package IDs
        packages_result = await db.execute(select(Package))
        packages = packages_result.scalars().all()

        if not packages:
            print("⚠ No packages found, skipping bookings...")
            return

        bookings = [
            EventBooking(
                full_name="Jessica Martinez",
                email="jessica.martinez@email.com",
                phone="+1-555-1234",
                event_type="Wedding",
                event_date=datetime.utcnow() + timedelta(days=90),
                expected_guests=120,
                venue_location="Sunset Garden, Downtown LA",
                package_id=packages[1].id
                if len(packages) > 1
                else None,  # Classic Package
                additional_details="Looking for outdoor ceremony with indoor reception. Prefer romantic garden theme.",
                special_requests="Vegetarian menu options needed for 20 guests",
                status="pending",
            ),
            EventBooking(
                full_name="Thomas Wilson",
                email="t.wilson@techcorp.com",
                phone="+1-555-5678",
                event_type="Corporate",
                event_date=datetime.utcnow() + timedelta(days=45),
                expected_guests=200,
                venue_location="Grand Conference Hall, Business District",
                package_id=packages[2].id
                if len(packages) > 2
                else None,  # Premium Package
                additional_details="Annual company gala dinner with awards ceremony",
                special_requests="Need AV equipment for presentations and projection screens",
                status="confirmed",
                admin_notes="Confirmed on phone. Deposit received.",
            ),
            EventBooking(
                full_name="Maria Garcia",
                email="maria.garcia@email.com",
                phone="+1-555-9012",
                event_type="Birthday",
                event_date=datetime.utcnow() + timedelta(days=30),
                expected_guests=75,
                venue_location="Lakeside Pavilion",
                package_id=packages[0].id
                if len(packages) > 0
                else None,  # Starter Package
                additional_details="Sweet 16 birthday party with DJ and dance floor",
                special_requests="Custom cake with photo design",
                status="pending",
            ),
        ]
        db.add_all(bookings)
        await db.commit()
        print(f"✓ {len(bookings)} sample bookings seeded successfully")


async def seed_translations():
    """Seed sample translations"""
    async with AsyncSessionLocal() as db:
        # Check if translations already exist
        result = await db.execute(select(Translation))
        existing_translations = result.scalars().all()

        if existing_translations:
            print("⚠ Translations already exist, skipping...")
            return

        translations = [
            Translation(
                entity_type="Package",
                entity_id=1,
                field_name="title",
                language="es",
                translated_text="Paquete Inicial",
            ),
            Translation(
                entity_type="Package",
                entity_id=1,
                field_name="description",
                language="es",
                translated_text="Perfecto para reuniones pequeñas e íntimas",
            ),
            Translation(
                entity_type="Package",
                entity_id=2,
                field_name="title",
                language="es",
                translated_text="Paquete Clásico",
            ),
            Translation(
                entity_type="Package",
                entity_id=2,
                field_name="title",
                language="fr",
                translated_text="Forfait Classique",
            ),
            Translation(
                entity_type="Theme",
                entity_id=1,
                field_name="name",
                language="es",
                translated_text="Jardín Romántico",
            ),
            Translation(
                entity_type="Theme",
                entity_id=1,
                field_name="description",
                language="es",
                translated_text="Elegante ambiente al aire libre con arreglos florales",
            ),
        ]
        db.add_all(translations)
        await db.commit()
        print(f"✓ {len(translations)} translations seeded successfully")


async def seed_all():
    """Run all seeders in order"""
    print("\n" + "=" * 50)
    print("SEEDING DATABASE")
    print("=" * 50 + "\n")

    await create_tables()
    await seed_users()
    await seed_packages()
    await seed_gallery()
    await seed_contact_info()
    await seed_contact_messages()
    await seed_themes()
    await seed_testimonials()
    await seed_sample_bookings()
    await seed_translations()

    print("\n" + "=" * 50)
    print("✓ Database seeding completed successfully!")
    print("=" * 50 + "\n")


if __name__ == "__main__":
    asyncio.run(seed_all())
