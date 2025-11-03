from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import JSON, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class GalleryItem(Base):
    """Gallery images with metadata for portfolio showcase"""

    __tablename__ = "gallery_items"

    id: Mapped[UUID] = mapped_column(primary_key=True, index=True, default=uuid4)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    image_url: Mapped[str] = mapped_column(nullable=False)
    thumbnail_url: Mapped[str | None]  # Optimized thumbnail for fast loading
    category_id: Mapped[UUID] = mapped_column(
        ForeignKey("gallery_categories.id"), nullable=False, index=True
    )
    tags: Mapped[list[str] | None] = mapped_column(
        JSON
    )  # JSON array of tags: ["outdoor", "elegant", "modern"]
    display_order: Mapped[int] = mapped_column(default=0)  # For manual sorting
    is_featured: Mapped[bool] = mapped_column(
        default=False, nullable=False
    )  # Featured on homepage
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    # Relationships
    category_obj = relationship("GalleryCategory", back_populates="gallery_items")
