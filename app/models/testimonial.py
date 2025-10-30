from uuid import UUID, uuid4

from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Testimonial(Base):
    __tablename__ = "testimonials"

    id: Mapped[UUID] = mapped_column(primary_key=True, index=True, default=uuid4)
    name: Mapped[str] = mapped_column(nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    image_url: Mapped[str | None]
    rating: Mapped[float] = mapped_column(nullable=False)  # e.g., 5.0
