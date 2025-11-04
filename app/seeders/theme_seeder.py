"""
Theme Seeder

Seeds event themes with actual images from seeders/images directory.
"""

import uuid
from pathlib import Path

from PIL import Image
from sqlalchemy import select

from app.models import Theme
from app.models.gallery_category import GalleryCategory

from .base import BaseSeeder
from .registry import registry

# Image processing configuration
UPLOAD_DIR = Path("uploads")
THEMES_DIR = UPLOAD_DIR / "themes"
SEEDER_IMAGES_DIR = Path(__file__).parent / "images"
MAX_IMAGE_SIZE = (2048, 2048)


def ensure_upload_directories():
    """Create upload directories if they don't exist."""
    THEMES_DIR.mkdir(parents=True, exist_ok=True)


def process_theme_image(source_path: Path) -> str:
    """
    Process an image from the seeders/images directory for themes.
    Converts to WebP format.

    Args:
        source_path: Path to the source image file

    Returns:
        Image URL
    """
    ensure_upload_directories()

    # Generate unique filename with .webp extension
    unique_filename = f"{uuid.uuid4()}.webp"
    image_path = THEMES_DIR / unique_filename

    try:
        with Image.open(source_path) as img:
            # Convert RGBA to RGB if necessary
            if img.mode in ("RGBA", "LA", "P"):
                background = Image.new("RGB", img.size, (255, 255, 255))
                if img.mode == "P":
                    img = img.convert("RGBA")
                background.paste(
                    img, mask=img.split()[-1] if img.mode == "RGBA" else None
                )
                img = background

            # Resize image if too large (maintain aspect ratio)
            img.thumbnail(MAX_IMAGE_SIZE, Image.Resampling.LANCZOS)

            # Save optimized image as WebP
            img.save(image_path, format="WEBP", optimize=True, quality=85)

    except Exception as e:
        # Clean up any created files on error
        if image_path.exists():
            image_path.unlink()
        raise ValueError(f"Failed to process image {source_path}: {str(e)}")

    # Return URL
    return f"/uploads/themes/{unique_filename}"


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
        """Create themes with actual images from seeders/images directory"""
        # Fetch category IDs by slug
        categories = {}
        for slug in ["weddings", "birthdays", "corporate-events", "anniversaries"]:
            result = await self.db.execute(
                select(GalleryCategory).where(GalleryCategory.slug == slug)
            )
            category = result.scalar_one_or_none()
            if category:
                categories[slug] = category.id

        # Define themes with their source images
        themes_data = [
            {
                "name": "Romantic Garden",
                "description": "Elegant outdoor setting with floral arrangements and soft lighting",
                "category": "weddings",
                "source_images": [
                    "garden-wedding-ceremony.jpg",
                    "elegant-wedding-reception.jpg",
                ],
            },
            {
                "name": "Modern Minimalist",
                "description": "Clean lines, contemporary design, and sophisticated aesthetics",
                "category": "weddings",
                "source_images": ["elegant-wedding-reception.jpg"],
            },
            {
                "name": "Classic Elegance",
                "description": "Timeless sophistication with luxurious details",
                "category": "anniversaries",
                "source_images": ["annyvercery.jpg"],
            },
            {
                "name": "Tropical Paradise",
                "description": "Vibrant colors, exotic flowers, and island-inspired decor",
                "category": "birthdays",
                "source_images": ["birthday-party-celebration.jpg"],
            },
            {
                "name": "Corporate Professional",
                "description": "Sleek and professional setup for business events",
                "category": "corporate-events",
                "source_images": ["corporate-gala-event.jpg"],
            },
        ]

        themes = []
        processed_count = 0
        skipped_count = 0

        for theme_data in themes_data:
            # Check if category exists
            category_id = categories.get(theme_data["category"])
            if not category_id:
                print(f"  - Skipping theme '{theme_data['name']}': category not found")
                skipped_count += 1
                continue

            # Process images for this theme
            gallery_images = []
            for source_image in theme_data["source_images"]:
                source_path = SEEDER_IMAGES_DIR / source_image
                if not source_path.exists():
                    print(
                        f"  - Warning: Image not found for theme '{theme_data['name']}': {source_image}"
                    )
                    continue

                try:
                    image_url = process_theme_image(source_path)
                    gallery_images.append(image_url)
                except Exception as e:
                    print(
                        f"  - Error processing image '{source_image}' for theme '{theme_data['name']}': {e}"
                    )
                    continue

            # Only create theme if we have at least one image
            if gallery_images:
                theme = Theme(
                    name=theme_data["name"],
                    description=theme_data["description"],
                    category_id=category_id,
                    gallery_images=gallery_images,
                )
                themes.append(theme)
                processed_count += 1
                print(
                    f"  - Created theme '{theme_data['name']}' with {len(gallery_images)} image(s)"
                )
            else:
                print(
                    f"  - Skipping theme '{theme_data['name']}': no valid images processed"
                )
                skipped_count += 1

        if themes:
            self.db.add_all(themes)
            await self.db.commit()
            print(
                f"  - Created {processed_count} themes with categories, skipped {skipped_count}"
            )
        else:
            print("  - No valid themes to create")


# Auto-register this seeder
registry.register(ThemeSeeder)
