"""
User Seeder

Seeds admin and sample users.
"""

from sqlalchemy import select

from app.models import User
from app.utils.auth import get_password_hash

from .base import BaseSeeder
from .registry import registry


class UserSeeder(BaseSeeder):
    """Seed admin and sample users"""

    name = "users"
    description = "Create admin and sample client users"
    dependencies = []

    async def should_run(self) -> bool:
        """Check if admin user already exists"""
        result = await self.db.execute(
            select(User).where(User.email == "admin@lushmoments.com")
        )
        return result.scalar_one_or_none() is None

    async def run(self) -> None:
        """Create admin and sample users"""
        # Create admin user
        admin = User(
            name="Admin User",
            email="admin@lushmoments.com",
            phone="+1234567890",
            password_hash=get_password_hash("Admin@123"),
            role="admin",
        )
        self.db.add(admin)

        # Create sample client user
        client = User(
            name="John Client",
            email="client@example.com",
            phone="+1987654321",
            password_hash=get_password_hash("Client@123"),
            role="client",
        )
        self.db.add(client)

        await self.db.commit()
        print("  - Admin: admin@lushmoments.com / Admin@123")
        print("  - Client: client@example.com / Client@123")


# Auto-register this seeder
registry.register(UserSeeder)
