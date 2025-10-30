from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class ContactMessage(Base):
    """Contact form submissions from 'Get in Touch' form"""

    __tablename__ = "contact_messages"

    id: Mapped[UUID] = mapped_column(primary_key=True, index=True, default=uuid4)
    full_name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, index=True)
    phone_number: Mapped[str] = mapped_column(nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    is_read: Mapped[bool] = mapped_column(default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
    responded_at: Mapped[datetime | None] = mapped_column(DateTime)
