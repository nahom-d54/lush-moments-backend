import asyncio

from app.database import AsyncSessionLocal, Base, engine
from app.models import Package, Testimonial, Theme, User
from app.utils.auth import get_password_hash


async def seed_data():
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as db:
        # Create admin user
        admin = User(
            name="Admin",
            email="admin@example.com",
            password_hash=get_password_hash("admin123"),
            role="admin",
        )
        db.add(admin)

        # Create sample packages
        packages = [
            Package(
                name="Basic Package",
                description="Basic event package",
                price=500.0,
                included_items="Venue, Catering",
            ),
            Package(
                name="Premium Package",
                description="Premium event package",
                price=1000.0,
                included_items="Venue, Catering, Photography",
            ),
        ]
        db.add_all(packages)

        # Create sample themes
        themes = [
            Theme(
                name="Romantic",
                description="Perfect for weddings",
                gallery_images="image1.jpg,image2.jpg",
            ),
            Theme(
                name="Corporate",
                description="For business events",
                gallery_images="image3.jpg",
            ),
        ]
        db.add_all(themes)

        # Create sample testimonials
        testimonials = [
            Testimonial(name="John Doe", message="Great service!", rating=5.0),
            Testimonial(name="Jane Smith", message="Highly recommend", rating=4.5),
        ]
        db.add_all(testimonials)

        await db.commit()
        print("Seed data added successfully")


if __name__ == "__main__":
    asyncio.run(seed_data())
