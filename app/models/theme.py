from sqlalchemy import JSON, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Theme(Base):
    __tablename__ = "themes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    gallery_images: Mapped[list[str] | None] = mapped_column(
        JSON
    )  # JSON string of image URLs
    featured: Mapped[bool] = mapped_column(default=False, nullable=False)
