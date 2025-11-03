from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models import BookingEnhancement, PackageEnhancement
from app.models import EventBooking as EventBookingModel
from app.models.event_booking import BookingStatus
from app.models.user import User
from app.schemas.event_booking import (
    BookingEnhancementResponse,
    EventBooking,
    EventBookingCreate,
    EventBookingResponse,
    EventBookingUpdate,
)
from app.utils.auth import get_current_user
from app.utils.email import send_booking_confirmation

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.post("/", response_model=EventBookingResponse)
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
    # prevent anonymous user from creating booking
    if current_user.isAnonymous:
        raise HTTPException(
            status_code=403,
            detail="Anonymous users are not allowed to create bookings. Please register or log in.",
        )
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
    await db.flush()  # Get booking ID

    # Add selected enhancements
    if booking.enhancements:
        for enhancement_selection in booking.enhancements:
            # Get enhancement to get current price
            enhancement_result = await db.execute(
                select(PackageEnhancement).where(
                    PackageEnhancement.id == enhancement_selection.enhancement_id
                )
            )
            enhancement = enhancement_result.scalar_one_or_none()

            if enhancement and enhancement.is_available:
                booking_enhancement = BookingEnhancement(
                    booking_id=db_booking.id,
                    enhancement_id=enhancement.id,
                    quantity=enhancement_selection.quantity,
                    price_at_booking=enhancement.starting_price,  # Store current price
                )
                db.add(booking_enhancement)

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


@router.get("/", response_model=list[EventBooking])
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
        .options(
            selectinload(EventBookingModel.booking_enhancements).selectinload(
                BookingEnhancement.enhancement
            )
        )
        .where(EventBookingModel.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .order_by(EventBookingModel.event_date.desc())
    )

    result = await db.execute(query)
    bookings = result.scalars().all()

    # Convert to response format with enhancement details
    booking_list = []
    for booking in bookings:
        # Build selected_enhancements from eager-loaded data
        selected_enhancements = [
            BookingEnhancementResponse(
                id=be.id,
                enhancement_id=be.enhancement.id,
                enhancement_name=be.enhancement.name,
                enhancement_description=be.enhancement.description,
                starting_price=be.enhancement.starting_price,
                quantity=be.quantity,
                price_at_booking=be.price_at_booking,
            )
            for be in booking.booking_enhancements
            if be.enhancement  # Enhancement may be None if deleted
        ]

        # Use model_validate to convert SQLAlchemy model to Pydantic
        booking_response = EventBooking.model_validate(
            booking, update={"selected_enhancements": selected_enhancements}
        )
        booking_list.append(booking_response)

    return booking_list


@router.get("/{booking_id}", response_model=EventBooking)
async def get_booking(
    booking_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Authenticated endpoint: Get a specific booking by ID.
    Users can only access their own bookings.
    """
    result = await db.execute(
        select(EventBookingModel)
        .options(
            selectinload(EventBookingModel.booking_enhancements).selectinload(
                BookingEnhancement.enhancement
            )
        )
        .where(EventBookingModel.id == booking_id)
    )
    booking = result.scalar_one_or_none()

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    # Verify ownership
    if booking.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to access this booking"
        )

    # Build selected_enhancements from eager-loaded data
    selected_enhancements = [
        BookingEnhancementResponse(
            id=be.id,
            enhancement_id=be.enhancement.id,
            enhancement_name=be.enhancement.name,
            enhancement_description=be.enhancement.description,
            starting_price=be.enhancement.starting_price,
            quantity=be.quantity,
            price_at_booking=be.price_at_booking,
        )
        for be in booking.booking_enhancements
        if be.enhancement  # Enhancement may be None if deleted
    ]

    # Use model_validate to convert SQLAlchemy model to Pydantic
    return EventBooking.model_validate(
        booking, update={"selected_enhancements": selected_enhancements}
    )


@router.put("/{booking_id}", response_model=EventBooking)
async def update_booking(
    booking_id: str,
    booking_update: EventBookingUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update a booking. Users can only update their own bookings and only when status is pending.
    """
    result = await db.execute(
        select(EventBookingModel)
        .options(
            selectinload(EventBookingModel.booking_enhancements).selectinload(
                BookingEnhancement.enhancement
            )
        )
        .where(EventBookingModel.id == booking_id)
    )
    booking = result.scalar_one_or_none()

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    # Verify ownership
    if booking.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to update this booking"
        )

    # Only allow editing if status is pending (unless admin updates status)
    if booking.status != BookingStatus.pending and booking_update.status is None:
        raise HTTPException(
            status_code=400,
            detail="Can only edit bookings with pending status. Please contact support for confirmed bookings.",
        )

    # Update fields
    if booking_update.event_type is not None:
        booking.event_type = booking_update.event_type
    if booking_update.event_date is not None:
        booking.event_date = booking_update.event_date
    if booking_update.expected_guests is not None:
        booking.expected_guests = booking_update.expected_guests
    if booking_update.venue_location is not None:
        booking.venue_location = booking_update.venue_location
    if booking_update.package_id is not None:
        booking.package_id = booking_update.package_id
    if booking_update.additional_details is not None:
        booking.additional_details = booking_update.additional_details
    if booking_update.special_requests is not None:
        booking.special_requests = booking_update.special_requests

    # Update enhancements if provided
    if booking_update.enhancements is not None:
        # Remove all existing enhancements
        await db.execute(
            select(BookingEnhancement).where(
                BookingEnhancement.booking_id == booking_id
            )
        )
        for be in booking.booking_enhancements:
            await db.delete(be)

        # Add new enhancements
        for enhancement_selection in booking_update.enhancements:
            enhancement_result = await db.execute(
                select(PackageEnhancement).where(
                    PackageEnhancement.id == enhancement_selection.enhancement_id
                )
            )
            enhancement = enhancement_result.scalar_one_or_none()

            if enhancement and enhancement.is_available:
                booking_enhancement = BookingEnhancement(
                    booking_id=booking.id,
                    enhancement_id=enhancement.id,
                    quantity=enhancement_selection.quantity,
                    price_at_booking=enhancement.starting_price,
                )
                db.add(booking_enhancement)

    # Admin can update status and notes
    if booking_update.status is not None:
        # This would typically require admin role check
        booking.status = booking_update.status
    if booking_update.admin_notes is not None:
        # This would typically require admin role check
        booking.admin_notes = booking_update.admin_notes

    await db.commit()
    await db.refresh(booking)

    # Build response
    return await get_booking(booking_id, db, current_user)
