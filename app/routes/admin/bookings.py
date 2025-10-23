from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import EventBooking
from app.schemas.event_booking import EventBooking as EventBookingSchema
from app.schemas.event_booking import EventBookingCreate, EventBookingUpdate
from app.utils.auth import get_current_admin

router = APIRouter(prefix="/admin/bookings", tags=["Admin - Bookings"])


@router.get("/", response_model=List[EventBookingSchema])
async def get_all_bookings(
    skip: int = 0,
    limit: int = 50,
    status: str = None,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    """Admin endpoint: Get all bookings with optional status filter"""
    query = (
        select(EventBooking)
        .offset(skip)
        .limit(limit)
        .order_by(EventBooking.event_date.desc())
    )

    if status:
        query = query.where(EventBooking.status == status)

    result = await db.execute(query)
    bookings = result.scalars().all()
    return bookings


@router.post("/", response_model=EventBookingSchema)
async def create_booking(
    booking: EventBookingCreate,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    db_booking = EventBooking(**booking.model_dump())
    db.add(db_booking)
    await db.commit()
    await db.refresh(db_booking)
    return db_booking


@router.get("/{booking_id}", response_model=EventBookingSchema)
async def get_booking(
    booking_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    result = await db.execute(select(EventBooking).where(EventBooking.id == booking_id))
    booking = result.scalar_one_or_none()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking


@router.patch("/{booking_id}", response_model=EventBookingSchema)
async def update_booking(
    booking_id: int,
    update_data: EventBookingUpdate,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    """Admin endpoint: Update booking status or add admin notes"""
    result = await db.execute(select(EventBooking).where(EventBooking.id == booking_id))
    db_booking = result.scalar_one_or_none()
    if not db_booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    # Update fields
    if update_data.status is not None:
        db_booking.status = update_data.status
    if update_data.admin_notes is not None:
        db_booking.admin_notes = update_data.admin_notes

    await db.commit()
    await db.refresh(db_booking)
    return db_booking


@router.delete("/{booking_id}")
async def delete_booking(
    booking_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    result = await db.execute(select(EventBooking).where(EventBooking.id == booking_id))
    booking = result.scalar_one_or_none()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    await db.delete(booking)
    await db.commit()
    return {"message": "Booking deleted successfully"}
