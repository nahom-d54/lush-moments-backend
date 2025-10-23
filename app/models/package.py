from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Package(Base):
    __tablename__ = "packages"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(nullable=False)  # Changed from 'name' to 'title'
    description: Mapped[str | None] = mapped_column(Text)
    price: Mapped[float] = mapped_column(nullable=False)
    is_popular: Mapped[bool] = mapped_column(
        default=False, nullable=False
    )  # Highlight popular packages
    display_order: Mapped[int] = mapped_column(default=0)  # For manual sorting

    # Relationships - items are stored as separate PackageItem records
    items = relationship(
        "PackageItem",
        back_populates="package",
        cascade="all, delete-orphan",
        order_by="PackageItem.display_order",
    )
