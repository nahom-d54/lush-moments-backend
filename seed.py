#!/usr/bin/env python3
"""
Database Seeder Runner

Run all or specific seeders to populate the database with initial data.

Usage:
    python seed.py                    # Run all seeders
    python seed.py users packages     # Run specific seeders
    python seed.py --list             # List all available seeders
"""

import argparse
import asyncio
import sys

from app.database import AsyncSessionLocal

# Import all seeders to auto-register them
from app.seeders import registry
from app.seeders.contact_info_seeder import ContactInfoSeeder  # noqa: F401
from app.seeders.enhancement_seeder import EnhancementSeeder  # noqa: F401
from app.seeders.faq_seeder import FAQSeeder  # noqa: F401
from app.seeders.gallery_seeder import GallerySeeder  # noqa: F401
from app.seeders.package_seeder import PackageSeeder  # noqa: F401
from app.seeders.testimonial_seeder import TestimonialSeeder  # noqa: F401
from app.seeders.theme_seeder import ThemeSeeder  # noqa: F401
from app.seeders.user_seeder import UserSeeder  # noqa: F401


async def main(seeder_names: list[str] | None = None):
    """
    Run database seeders.

    Args:
        seeder_names: List of specific seeder names to run, or None to run all
    """
    async with AsyncSessionLocal() as db:
        try:
            await registry.run_all(db, seeder_names)
        except ValueError as e:
            print(f"\n❌ Error: {e}\n")
            sys.exit(1)
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}\n")
            await db.rollback()
            raise


def list_seeders():
    """List all available seeders"""
    print("\n" + "=" * 60)
    print("AVAILABLE SEEDERS")
    print("=" * 60 + "\n")

    for name, description in registry.list_seeders():
        print(f"  {name:20s} - {description}")

    print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run database seeders",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python seed.py                    # Run all seeders
  python seed.py users packages     # Run specific seeders
  python seed.py --list             # List available seeders
        """,
    )

    parser.add_argument(
        "seeders",
        nargs="*",
        help="Names of specific seeders to run (leave empty to run all)",
    )

    parser.add_argument(
        "--list", "-l", action="store_true", help="List all available seeders"
    )

    args = parser.parse_args()

    if args.list:
        list_seeders()
    else:
        seeder_names = args.seeders if args.seeders else None
        asyncio.run(main(seeder_names))
