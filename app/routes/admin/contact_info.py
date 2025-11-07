from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.contact_info import ContactInfo
from app.schemas.contact_info import (
    ContactInfo as ContactInfoSchema,
)
from app.schemas.contact_info import (
    ContactInfoCreate,
    ContactInfoUpdate,
)
from app.utils.auth import get_current_admin

router = APIRouter(prefix="/admin/contact-info", tags=["Contact Info"])


@router.post("/", response_model=ContactInfoSchema)
@router.post("", response_model=ContactInfoSchema)
async def create_contact_info(
    info: ContactInfoCreate,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    """
    Admin endpoint: Create business contact information.
    Should only be called once during initial setup.
    """
    # Check if contact info already exists
    result = await db.execute(select(ContactInfo).limit(1))
    existing = result.scalar_one_or_none()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Contact info already exists. Use PATCH to update it.",
        )

    db_info = ContactInfo(
        email=info.email,
        phone=info.phone,
        location=info.location,
        business_hours=info.business_hours,
        secondary_phone=info.secondary_phone,
        secondary_email=info.secondary_email,
        facebook_url=info.facebook_url,
        instagram_url=info.instagram_url,
        twitter_url=info.twitter_url,
        linkedin_url=info.linkedin_url,
        google_maps_url=info.google_maps_url,
    )
    db.add(db_info)
    await db.commit()
    await db.refresh(db_info)
    return db_info


@router.patch("/", response_model=ContactInfoSchema)
@router.patch("", response_model=ContactInfoSchema)
async def update_contact_info(
    update_data: ContactInfoUpdate,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    """
    Admin endpoint: Update business contact information.
    Updates the first (and typically only) contact info record.
    """
    result = await db.execute(select(ContactInfo).limit(1))
    contact_info = result.scalar_one_or_none()

    if not contact_info:
        raise HTTPException(
            status_code=404,
            detail="Contact info not found. Use POST to create it first.",
        )

    # Update fields
    update_dict = update_data.model_dump(exclude_unset=True)
    for field, value in update_dict.items():
        setattr(contact_info, field, value)

    await db.commit()
    await db.refresh(contact_info)

    return contact_info


@router.delete("/")
@router.delete("")
async def delete_contact_info(
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    """Admin endpoint: Delete contact information (rarely needed)"""
    result = await db.execute(select(ContactInfo).limit(1))
    contact_info = result.scalar_one_or_none()

    if not contact_info:
        raise HTTPException(status_code=404, detail="Contact info not found")

    await db.delete(contact_info)
    await db.commit()

    return {"message": "Contact information deleted successfully"}
