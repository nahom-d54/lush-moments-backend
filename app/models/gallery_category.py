from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class GalleryCategory(Base):
    """Gallery categories for organizing gallery items"""

    __tablename__ = "gallery_categories"

    id: Mapped[UUID] = mapped_column(primary_key=True, index=True, default=uuid4)
    name: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    slug: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    description: Mapped[str | None]
    display_order: Mapped[int] = mapped_column(default=0)  # For sorting
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationships
    gallery_items = relationship("GalleryItem", back_populates="category_obj")
