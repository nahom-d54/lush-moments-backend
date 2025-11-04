"""
Gallery Seeder

Seeds gallery items with actual images from seeders/images directory.
"""

import uuid
from pathlib import Path

from PIL import Image
from sqlalchemy import select

from app.models import GalleryItem
from app.models.gallery_category import GalleryCategory

from .base import BaseSeeder
from .registry import registry

# Image processing configuration
UPLOAD_DIR = Path("uploads")
GALLERY_DIR = UPLOAD_DIR / "gallery"
THUMBNAIL_DIR = GALLERY_DIR / "thumbnails"
SEEDER_IMAGES_DIR = Path(__file__).parent / "images"
MAX_IMAGE_SIZE = (2048, 2048)
THUMBNAIL_SIZE = (400, 400)


def ensure_upload_directories():
    """Create upload directories if they don't exist."""
    GALLERY_DIR.mkdir(parents=True, exist_ok=True)
    THUMBNAIL_DIR.mkdir(parents=True, exist_ok=True)


def process_seeder_image(source_path: Path) -> tuple[str, str]:
    """
    Process an image from the seeders/images directory.
    Converts to WebP format and creates a thumbnail.

    Args:
        source_path: Path to the source image file

    Returns:
        Tuple of (image_url, thumbnail_url)
    """
    ensure_upload_directories()

    # Generate unique filename with .webp extension
    unique_filename = f"{uuid.uuid4()}.webp"
    image_path = GALLERY_DIR / unique_filename
    thumbnail_path = THUMBNAIL_DIR / unique_filename

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

            # Resize main image if too large (maintain aspect ratio)
            img.thumbnail(MAX_IMAGE_SIZE, Image.Resampling.LANCZOS)

            # Save optimized main image as WebP
            img.save(image_path, format="WEBP", optimize=True, quality=85)

            # Create and save thumbnail as WebP
            img_thumb = img.copy()
            img_thumb.thumbnail(THUMBNAIL_SIZE, Image.Resampling.LANCZOS)
            img_thumb.save(thumbnail_path, format="WEBP", optimize=True, quality=85)

    except Exception as e:
        # Clean up any created files on error
        if image_path.exists():
            image_path.unlink()
        if thumbnail_path.exists():
            thumbnail_path.unlink()
        raise ValueError(f"Failed to process image {source_path}: {str(e)}")

    # Return URLs
    image_url = f"/uploads/gallery/{unique_filename}"
    thumbnail_url = f"/uploads/gallery/thumbnails/{unique_filename}"

    return image_url, thumbnail_url


class GallerySeeder(BaseSeeder):
    """Seed gallery items"""

    name = "gallery"
    description = "Create gallery items"
    dependencies = ["gallery_categories"]  # Must run after categories are created

    async def should_run(self) -> bool:
        """Check if gallery items already exist"""
        result = await self.db.execute(select(GalleryItem).limit(1))
        return result.first() is None

    async def run(self) -> None:
        """Create gallery items with actual images from seeders/images directory"""
        # Get category IDs by slug
        categories = {}
        for slug in ["weddings", "corporate-events", "birthdays", "anniversaries"]:
            result = await self.db.execute(
                select(GalleryCategory).where(GalleryCategory.slug == slug)
            )
            category = result.scalar_one_or_none()
            if category:
                categories[slug] = category.id

        if not categories:
            print("  - No categories found, skipping gallery items")
            return

        # Define gallery items with their source images
        gallery_data = [
            {
                "title": "Elegant Wedding Reception",
                "description": "Beautiful wedding setup with romantic lighting and floral arrangements",
                "source_image": "elegant-wedding-reception.jpg",
                "category": "weddings",
                "tags": ["wedding", "elegant", "romantic", "indoor"],
                "is_featured": True,
                "display_order": 1,
            },
            {
                "title": "Corporate Gala Event",
                "description": "Professional corporate event with modern setup",
                "source_image": "corporate-gala-event.jpg",
                "category": "corporate-events",
                "tags": ["corporate", "professional", "modern"],
                "is_featured": True,
                "display_order": 2,
            },
            {
                "title": "Birthday Party Celebration",
                "description": "Colorful and vibrant birthday party setup",
                "source_image": "birthday-party-celebration.jpg",
                "category": "birthdays",
                "tags": ["birthday", "colorful", "fun", "outdoor"],
                "is_featured": False,
                "display_order": 3,
            },
            {
                "title": "Garden Wedding Ceremony",
                "description": "Outdoor garden wedding with natural beauty",
                "source_image": "garden-wedding-ceremony.jpg",
                "category": "weddings",
                "tags": ["wedding", "outdoor", "garden", "natural"],
                "is_featured": True,
                "display_order": 4,
            },
            {
                "title": "Anniversary Dinner Setup",
                "description": "Intimate anniversary celebration with elegant table settings",
                "source_image": "annyvercery.jpg",
                "category": "anniversaries",
                "tags": ["anniversary", "intimate", "elegant"],
                "is_featured": False,
                "display_order": 5,
            },
        ]

        gallery_items = []
        processed_count = 0
        skipped_count = 0

        for item_data in gallery_data:
            # Check if category exists
            category_id = categories.get(item_data["category"])
            if not category_id:
                print(f"  - Skipping '{item_data['title']}': category not found")
                skipped_count += 1
                continue

            # Check if source image exists
            source_path = SEEDER_IMAGES_DIR / item_data["source_image"]
            if not source_path.exists():
                print(
                    f"  - Skipping '{item_data['title']}': image not found at {source_path}"
                )
                skipped_count += 1
                continue

            try:
                # Process the image
                image_url, thumbnail_url = process_seeder_image(source_path)

                # Create gallery item
                gallery_item = GalleryItem(
                    title=item_data["title"],
                    description=item_data["description"],
                    image_url=image_url,
                    thumbnail_url=thumbnail_url,
                    category_id=category_id,
                    tags=item_data["tags"],
                    is_featured=item_data["is_featured"],
                    display_order=item_data["display_order"],
                )
                gallery_items.append(gallery_item)
                processed_count += 1
                print(f"  - Processed '{item_data['title']}' -> {image_url}")

            except Exception as e:
                print(f"  - Error processing '{item_data['title']}': {e}")
                skipped_count += 1
                continue

        if gallery_items:
            self.db.add_all(gallery_items)
            await self.db.commit()
            print(
                f"  - Created {processed_count} gallery items, skipped {skipped_count}"
            )
        else:
            print("  - No valid gallery items to create")


# Auto-register this seeder
registry.register(GallerySeeder)
