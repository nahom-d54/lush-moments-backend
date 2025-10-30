from uuid import UUID, uuid4

from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class PackageEnhancement(Base):
    """Add-on enhancements that can be added to any package"""

    __tablename__ = "package_enhancements"

    id: Mapped[UUID] = mapped_column(primary_key=True, index=True, default=uuid4)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    starting_price: Mapped[float] = mapped_column(nullable=False)
    category: Mapped[str | None] = (
        mapped_column()
    )  # e.g., "floral", "entertainment", "decor"
    icon: Mapped[str | None] = mapped_column()  # Icon name or emoji
    is_available: Mapped[bool] = mapped_column(default=True, nullable=False)
    display_order: Mapped[int] = mapped_column(default=0)
