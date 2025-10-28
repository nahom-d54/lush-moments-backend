from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.contact_message import ContactMessage
from app.schemas.contact_message import (
    ContactMessage as ContactMessageSchema,
)
from app.schemas.contact_message import (
    ContactMessageUpdate,
)
from app.utils.auth import get_current_admin

router = APIRouter(prefix="/admin/contact", tags=["Contact"])


@router.get("/messages", response_model=list[ContactMessageSchema])
async def get_contact_messages(
    skip: int = 0,
    limit: int = 50,
    unread_only: bool = False,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    """
    Admin endpoint: Get all contact form submissions.
    Filter by unread messages if specified.
    """
    query = (
        select(ContactMessage)
        .offset(skip)
        .limit(limit)
        .order_by(ContactMessage.created_at.desc())
    )

    if unread_only:
        query = query.where(ContactMessage.is_read.is_(False))

    result = await db.execute(query)
    messages = result.scalars().all()
    return messages


@router.get("/messages/{message_id}", response_model=ContactMessageSchema)
async def get_contact_message(
    message_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    """Admin endpoint: Get a specific contact message"""
    result = await db.execute(
        select(ContactMessage).where(ContactMessage.id == message_id)
    )
    message = result.scalar_one_or_none()

    if not message:
        raise HTTPException(status_code=404, detail="Message not found")

    return message


@router.patch("/messages/{message_id}", response_model=ContactMessageSchema)
async def update_contact_message(
    message_id: int,
    update_data: ContactMessageUpdate,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    """Admin endpoint: Mark message as read or update response date"""
    result = await db.execute(
        select(ContactMessage).where(ContactMessage.id == message_id)
    )
    message = result.scalar_one_or_none()

    if not message:
        raise HTTPException(status_code=404, detail="Message not found")

    # Update fields
    if update_data.is_read is not None:
        message.is_read = update_data.is_read
    if update_data.responded_at is not None:
        message.responded_at = update_data.responded_at

    await db.commit()
    await db.refresh(message)

    return message


@router.delete("/messages/{message_id}")
async def delete_contact_message(
    message_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    """Admin endpoint: Delete a contact message"""
    result = await db.execute(
        select(ContactMessage).where(ContactMessage.id == message_id)
    )
    message = result.scalar_one_or_none()

    if not message:
        raise HTTPException(status_code=404, detail="Message not found")

    await db.delete(message)
    await db.commit()

    return {"message": "Contact message deleted successfully"}
