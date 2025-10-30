from uuid import UUID, uuid4

from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class FAQ(Base):
    """Frequently Asked Questions"""

    __tablename__ = "faqs"

    id: Mapped[UUID] = mapped_column(primary_key=True, index=True, default=uuid4)
    question: Mapped[str] = mapped_column(nullable=False)
    answer: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str | None] = (
        mapped_column()
    )  # e.g., "payment", "delivery", "customization"
    display_order: Mapped[int] = mapped_column(default=0)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
