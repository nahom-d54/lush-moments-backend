"""
Booking Enhancement Model

Links event bookings to selected package enhancements.
"""

from uuid import UUID, uuid4

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class BookingEnhancement(Base):
    """
    Many-to-many relationship between EventBooking and PackageEnhancement.
    Tracks which enhancements were added to each booking.
    """

    __tablename__ = "booking_enhancements"

    id: Mapped[UUID] = mapped_column(primary_key=True, index=True, default=uuid4)

    # Foreign Keys
    booking_id: Mapped[UUID] = mapped_column(
        ForeignKey("event_bookings.id", ondelete="CASCADE"), nullable=False, index=True
    )
    enhancement_id: Mapped[UUID] = mapped_column(
        ForeignKey("package_enhancements.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Optional: quantity if enhancements can be ordered multiple times
    quantity: Mapped[int] = mapped_column(default=1, nullable=False)

    # Optional: custom price at time of booking (in case prices change)
    price_at_booking: Mapped[float | None] = mapped_column()

    # Relationships
    booking = relationship("EventBooking", back_populates="booking_enhancements")
    enhancement = relationship("PackageEnhancement")
