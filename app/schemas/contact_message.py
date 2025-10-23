from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class ContactMessageBase(BaseModel):
    full_name: str
    email: EmailStr
    phone_number: str
    message: str


class ContactMessageCreate(ContactMessageBase):
    """Schema for creating a new contact message (public endpoint)"""

    pass


class ContactMessageResponse(BaseModel):
    """Response after submitting contact form"""

    message: str
    id: int


class ContactMessage(ContactMessageBase):
    """Full contact message details (admin view)"""

    id: int
    is_read: bool
    created_at: datetime
    responded_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ContactMessageUpdate(BaseModel):
    """For marking as read or adding response date"""

    is_read: Optional[bool] = None
    responded_at: Optional[datetime] = None
