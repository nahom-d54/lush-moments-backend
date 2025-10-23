from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.contact_message import ContactMessage
from app.schemas.contact_message import (
    ContactMessageCreate,
    ContactMessageResponse,
)
from app.utils.email import send_contact_form_notification

router = APIRouter(prefix="/contact", tags=["Contact"])


@router.post("/", response_model=ContactMessageResponse)
async def submit_contact_form(
    message: ContactMessageCreate, db: AsyncSession = Depends(get_db)
):
    """
    Public endpoint for submitting the 'Get in Touch' contact form.
    Sends confirmation email to user and notification to admin.
    """
    # Create contact message
    db_message = ContactMessage(
        full_name=message.full_name,
        email=message.email,
        phone_number=message.phone_number,
        message=message.message,
    )
    db.add(db_message)
    await db.commit()
    await db.refresh(db_message)

    # Send email notifications (async, don't block response)
    await send_contact_form_notification(
        user_name=message.full_name,
        user_email=message.email,
        user_phone=message.phone_number,
        message=message.message,
    )

    return ContactMessageResponse(
        message="Thank you for contacting us! We'll get back to you soon.",
        id=db_message.id,
    )
