from uuid import UUID, uuid4

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class PackageItem(Base):
    """Individual items/features included in a package"""

    __tablename__ = "package_items"

    id: Mapped[UUID] = mapped_column(primary_key=True, index=True, default=uuid4)
    package_id: Mapped[UUID] = mapped_column(
        ForeignKey("packages.id", ondelete="CASCADE"), nullable=False
    )
    item_text: Mapped[str] = mapped_column(nullable=False)
    display_order: Mapped[int] = mapped_column(default=0)

    # Relationships
    package = relationship("Package", back_populates="items")
