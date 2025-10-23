import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class BookingStatus(enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    completed = "completed"
    cancelled = "cancelled"


class EventBooking(Base):
    __tablename__ = "event_bookings"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # User Reference (Required - authenticated users only)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False, index=True
    )

    # User Information (cached for reference)
    full_name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, index=True)
    phone: Mapped[str] = mapped_column(nullable=False)

    # Event Information
    event_type: Mapped[str] = mapped_column(
        nullable=False
    )  # dropdown: wedding, birthday, corporate, etc.
    event_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    expected_guests: Mapped[int] = mapped_column(nullable=False)
    venue_location: Mapped[str] = mapped_column(nullable=False)

    # Package Selection
    package_id: Mapped[int | None] = mapped_column(ForeignKey("packages.id"))

    # Additional Details
    additional_details: Mapped[str | None] = mapped_column(Text)
    special_requests: Mapped[str | None] = mapped_column(Text)

    # Booking Management
    status: Mapped[BookingStatus] = mapped_column(
        Enum(BookingStatus), default=BookingStatus.pending, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime, onupdate=datetime.utcnow
    )
    admin_notes: Mapped[str | None] = mapped_column(Text)  # Internal notes for admins

    # Relationships
    user = relationship("User", back_populates="bookings")
    package = relationship("Package")
