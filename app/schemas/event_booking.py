from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr

from app.models.event_booking import BookingStatus


class EnhancementSelection(BaseModel):
    """Schema for selecting an enhancement"""

    enhancement_id: UUID
    quantity: int = 1


class BookingEnhancementResponse(BaseModel):
    """Response schema for booking enhancement"""

    id: UUID
    enhancement_id: UUID
    enhancement_name: str
    enhancement_description: str
    starting_price: float
    quantity: int
    price_at_booking: Optional[float] = None

    class Config:
        from_attributes = True


class EventBookingBase(BaseModel):
    # Event Information
    event_type: str  # Wedding, Birthday, Corporate, Anniversary, etc.
    event_date: datetime
    expected_guests: int
    venue_location: str

    # Package Selection
    package_id: Optional[UUID] = None

    # Additional Details
    additional_details: Optional[str] = None
    special_requests: Optional[str] = None

    # Enhancements Selection
    enhancements: list[EnhancementSelection] = []


class EventBookingCreate(EventBookingBase):
    """
    Schema for creating a new booking (authenticated users).
    User info is optional - will use authenticated user's data if not provided.
    """

    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None


class EventBookingUpdate(BaseModel):
    """Schema for updating booking (users can edit pending bookings, admin can update status)"""

    # Fields users can update when status is pending
    event_type: Optional[str] = None
    event_date: Optional[datetime] = None
    expected_guests: Optional[int] = None
    venue_location: Optional[str] = None
    package_id: Optional[UUID] = None
    additional_details: Optional[str] = None
    special_requests: Optional[str] = None
    enhancements: Optional[list[EnhancementSelection]] = None

    # Admin-only fields
    status: Optional[BookingStatus] = None
    admin_notes: Optional[str] = None


class EventBooking(EventBookingBase):
    """Full booking details"""

    id: UUID
    user_id: UUID
    full_name: str
    email: str
    phone: str
    status: BookingStatus
    created_at: datetime
    updated_at: Optional[datetime] = None
    admin_notes: Optional[str] = None
    selected_enhancements: list[BookingEnhancementResponse] = []

    class Config:
        from_attributes = True


class EventBookingResponse(BaseModel):
    """Response after creating a booking"""

    message: str
    booking_id: UUID
    confirmation_email_sent: bool
