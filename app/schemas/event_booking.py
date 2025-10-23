from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class EventBookingBase(BaseModel):
    # Event Information
    event_type: str  # Wedding, Birthday, Corporate, Anniversary, etc.
    event_date: datetime
    expected_guests: int
    venue_location: str

    # Package Selection
    package_id: Optional[int] = None

    # Additional Details
    additional_details: Optional[str] = None
    special_requests: Optional[str] = None


class EventBookingCreate(EventBookingBase):
    """
    Schema for creating a new booking (authenticated users).
    User info is optional - will use authenticated user's data if not provided.
    """

    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None


class EventBookingUpdate(BaseModel):
    """Schema for updating booking (admin can update status and notes)"""

    status: Optional[str] = None
    admin_notes: Optional[str] = None


class EventBooking(EventBookingBase):
    """Full booking details"""

    id: int
    user_id: int
    full_name: str
    email: str
    phone: str
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    admin_notes: Optional[str] = None

    class Config:
        from_attributes = True


class EventBookingResponse(BaseModel):
    """Response after creating a booking"""

    message: str
    booking_id: int
    confirmation_email_sent: bool
