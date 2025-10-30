from typing import Dict
from uuid import UUID, uuid4

from sqlalchemy import JSON, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class ContactInfo(Base):
    """Business contact information and hours - typically only one record"""

    __tablename__ = "contact_info"

    id: Mapped[UUID] = mapped_column(primary_key=True, index=True, default=uuid4)
    email: Mapped[str] = mapped_column(nullable=False)
    phone: Mapped[str] = mapped_column(nullable=False)
    location: Mapped[str] = mapped_column(
        Text, nullable=False
    )  # Full address with city, state, zip
    business_hours: Mapped[Dict[str, str]] = mapped_column(
        JSON, nullable=False
    )  # JSON: {"monday": "9:00 AM - 6:00 PM", ...}
    secondary_phone: Mapped[str | None]
    secondary_email: Mapped[str | None]
    facebook_url: Mapped[str | None]
    instagram_url: Mapped[str | None]
    twitter_url: Mapped[str | None]
    linkedin_url: Mapped[str | None]
    google_maps_url: Mapped[str | None]
