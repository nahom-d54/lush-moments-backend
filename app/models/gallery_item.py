from datetime import datetime

from sqlalchemy import DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class GalleryItem(Base):
    """Gallery images with metadata for portfolio showcase"""

    __tablename__ = "gallery_items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    image_url: Mapped[str] = mapped_column(nullable=False)
    thumbnail_url: Mapped[str | None]  # Optimized thumbnail for fast loading
    category: Mapped[str] = mapped_column(
        nullable=False, index=True
    )  # e.g., "wedding", "birthday", "corporate"
    tags: Mapped[str | None] = mapped_column(
        Text
    )  # JSON array of tags: ["outdoor", "elegant", "modern"]
    display_order: Mapped[int] = mapped_column(default=0)  # For manual sorting
    is_featured: Mapped[bool] = mapped_column(
        default=False, nullable=False
    )  # Featured on homepage
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
