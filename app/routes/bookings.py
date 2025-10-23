from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import EventBooking as EventBookingModel
from app.models.user import User
from app.schemas.event_booking import (
    EventBooking,
    EventBookingCreate,
    EventBookingResponse,
)
from app.utils.auth import get_current_user
from app.utils.email import send_booking_confirmation

router = APIRouter()


@router.post("/bookings", response_model=EventBookingResponse)
async def create_booking(
    booking: EventBookingCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Authenticated endpoint for creating event bookings.
    Requires user to be logged in.
    Sends confirmation email to customer and notification to admin.
    """
    # Create booking with user_id
    db_booking = EventBookingModel(
        user_id=current_user.id,
        full_name=booking.full_name or current_user.name,
        email=booking.email or current_user.email,
        phone=booking.phone or current_user.phone or "",
        event_type=booking.event_type,
        event_date=booking.event_date,
        expected_guests=booking.expected_guests,
        package_id=booking.package_id,
        venue_location=booking.venue_location,
        additional_details=booking.additional_details,
        special_requests=booking.special_requests,
    )
    db.add(db_booking)
    await db.commit()
    await db.refresh(db_booking)

    # Send confirmation emails in background
    email_sent = False
    try:
        background_tasks.add_task(
            send_booking_confirmation,
            user_name=db_booking.full_name,
            user_email=db_booking.email,
            event_type=booking.event_type,
            event_date=booking.event_date.strftime("%B %d, %Y at %I:%M %p"),
            booking_id=db_booking.id,
        )
        email_sent = True
    except Exception as e:
        print(f"Error scheduling notification: {e}")

    return EventBookingResponse(
        message="Your booking request has been submitted successfully! You'll receive a confirmation email shortly.",
        booking_id=db_booking.id,
        confirmation_email_sent=email_sent,
    )


@router.get("/bookings", response_model=list[EventBooking])
async def get_user_bookings(
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Authenticated endpoint: Get bookings for the current logged-in user.
    Users can only see their own bookings.
    """
    query = (
        select(EventBookingModel)
        .where(EventBookingModel.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .order_by(EventBookingModel.event_date.desc())
    )

    result = await db.execute(query)
    bookings = result.scalars().all()
    return bookings


@router.get("/bookings/{booking_id}", response_model=EventBooking)
async def get_booking(
    booking_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Authenticated endpoint: Get a specific booking by ID.
    Users can only access their own bookings.
    """
    result = await db.execute(
        select(EventBookingModel).where(EventBookingModel.id == booking_id)
    )
    booking = result.scalar_one_or_none()

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    # Verify ownership
    if booking.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to access this booking"
        )

    return booking
