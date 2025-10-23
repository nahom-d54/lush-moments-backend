from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.contact_info import ContactInfo
from app.schemas.contact_info import (
    ContactInfo as ContactInfoSchema,
)

router = APIRouter(prefix="/contact-info", tags=["Contact Info"])


@router.get("/", response_model=ContactInfoSchema)
async def get_contact_info(db: AsyncSession = Depends(get_db)):
    """
    Public endpoint: Get business contact information.
    Returns the first (and typically only) contact info record.
    """
    result = await db.execute(select(ContactInfo).limit(1))
    contact_info = result.scalar_one_or_none()

    if not contact_info:
        raise HTTPException(
            status_code=404,
            detail="Contact information not configured. Please ask admin to set it up.",
        )

    return contact_info
