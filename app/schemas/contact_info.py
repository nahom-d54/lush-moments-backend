from typing import Optional

from pydantic import BaseModel, EmailStr


class ContactInfoBase(BaseModel):
    email: EmailStr
    phone: str
    location: str
    business_hours: str  # JSON string
    secondary_phone: Optional[str] = None
    secondary_email: Optional[EmailStr] = None
    facebook_url: Optional[str] = None
    instagram_url: Optional[str] = None
    twitter_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    google_maps_url: Optional[str] = None


class ContactInfoCreate(ContactInfoBase):
    pass


class ContactInfoUpdate(BaseModel):
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    business_hours: Optional[str] = None
    secondary_phone: Optional[str] = None
    secondary_email: Optional[EmailStr] = None
    facebook_url: Optional[str] = None
    instagram_url: Optional[str] = None
    twitter_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    google_maps_url: Optional[str] = None


class ContactInfo(ContactInfoBase):
    id: int

    class Config:
        from_attributes = True
