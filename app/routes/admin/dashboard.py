from typing import Any, Dict

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import (
    FAQ,
    ContactMessage,
    EventBooking,
    GalleryCategory,
    GalleryItem,
    Package,
    PackageEnhancement,
    Session,
    Testimonial,
    Theme,
    User,
)
from app.models.event_booking import BookingStatus
from app.schemas.dashboard import DashboardStatsResponse
from app.utils.auth import get_current_admin

router = APIRouter(prefix="/admin/dashboard", tags=["Admin Dashboard"])


@router.get("/stats", response_model=DashboardStatsResponse)
async def get_dashboard_stats(
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin),
) -> Dict[str, Any]:
    """
    Admin endpoint: Get comprehensive dashboard statistics.

    Returns counts and breakdowns for:
    - Bookings (total and by status)
    - Users
    - Packages
    - Themes
    - Gallery items
    - Testimonials
    - Contact messages
    - Chat sessions
    - FAQs
    - Enhancements
    """

    # Bookings statistics
    total_bookings = await db.scalar(select(func.count(EventBooking.id)))

    pending_bookings = await db.scalar(
        select(func.count(EventBooking.id)).where(
            EventBooking.status == BookingStatus.pending
        )
    )

    confirmed_bookings = await db.scalar(
        select(func.count(EventBooking.id)).where(
            EventBooking.status == BookingStatus.confirmed
        )
    )

    completed_bookings = await db.scalar(
        select(func.count(EventBooking.id)).where(
            EventBooking.status == BookingStatus.completed
        )
    )

    cancelled_bookings = await db.scalar(
        select(func.count(EventBooking.id)).where(
            EventBooking.status == BookingStatus.cancelled
        )
    )

    # Users statistics
    total_users = await db.scalar(select(func.count(User.id)))

    admin_users = await db.scalar(
        select(func.count(User.id)).where(User.role == "admin")
    )

    client_users = await db.scalar(
        select(func.count(User.id)).where(User.role == "client")
    )

    anonymous_users = await db.scalar(
        select(func.count(User.id)).where(User.is_anonymous == True)
    )

    # Packages statistics
    total_packages = await db.scalar(select(func.count(Package.id)))

    # Themes statistics
    total_themes = await db.scalar(select(func.count(Theme.id)))

    featured_themes = await db.scalar(
        select(func.count(Theme.id)).where(Theme.featured == True)
    )

    # Gallery statistics
    total_gallery_items = await db.scalar(select(func.count(GalleryItem.id)))

    featured_gallery_items = await db.scalar(
        select(func.count(GalleryItem.id)).where(GalleryItem.is_featured == True)
    )

    total_gallery_categories = await db.scalar(select(func.count(GalleryCategory.id)))

    active_gallery_categories = await db.scalar(
        select(func.count(GalleryCategory.id)).where(GalleryCategory.is_active == True)
    )

    # Testimonials statistics
    total_testimonials = await db.scalar(select(func.count(Testimonial.id)))

    # Contact messages statistics
    total_contact_messages = await db.scalar(select(func.count(ContactMessage.id)))

    unread_contact_messages = await db.scalar(
        select(func.count(ContactMessage.id)).where(ContactMessage.is_read == False)
    )

    responded_contact_messages = await db.scalar(
        select(func.count(ContactMessage.id)).where(
            ContactMessage.responded_at.isnot(None)
        )
    )

    # Chat sessions statistics
    total_sessions = await db.scalar(select(func.count(Session.id)))

    bot_handled_sessions = await db.scalar(
        select(func.count(Session.id)).where(Session.is_handled_by_agent == True)
    )

    human_transferred_sessions = await db.scalar(
        select(func.count(Session.id)).where(Session.transferred_to_human == True)
    )

    # FAQs statistics
    total_faqs = await db.scalar(select(func.count(FAQ.id)))

    active_faqs = await db.scalar(
        select(func.count(FAQ.id)).where(FAQ.is_active == True)
    )

    # Enhancements statistics
    total_enhancements = await db.scalar(select(func.count(PackageEnhancement.id)))

    available_enhancements = await db.scalar(
        select(func.count(PackageEnhancement.id)).where(
            PackageEnhancement.is_available == True
        )
    )

    # Get recent bookings count (last 30 days)
    from datetime import datetime, timedelta, timezone

    thirty_days_ago = datetime.now(timezone.utc) - timedelta(days=30)

    recent_bookings = await db.scalar(
        select(func.count(EventBooking.id)).where(
            EventBooking.created_at >= thirty_days_ago
        )
    )

    # Get recent contact messages count (last 7 days)
    seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)

    recent_contact_messages = await db.scalar(
        select(func.count(ContactMessage.id)).where(
            ContactMessage.created_at >= seven_days_ago
        )
    )

    return {
        "bookings": {
            "total": total_bookings or 0,
            "by_status": {
                "pending": pending_bookings or 0,
                "confirmed": confirmed_bookings or 0,
                "completed": completed_bookings or 0,
                "cancelled": cancelled_bookings or 0,
            },
            "recent_30_days": recent_bookings or 0,
        },
        "users": {
            "total": total_users or 0,
            "admins": admin_users or 0,
            "clients": client_users or 0,
            "anonymous": anonymous_users or 0,
        },
        "packages": {
            "total": total_packages or 0,
        },
        "themes": {
            "total": total_themes or 0,
            "featured": featured_themes or 0,
        },
        "gallery": {
            "total_items": total_gallery_items or 0,
            "featured_items": featured_gallery_items or 0,
            "total_categories": total_gallery_categories or 0,
            "active_categories": active_gallery_categories or 0,
        },
        "testimonials": {
            "total": total_testimonials or 0,
        },
        "contact_messages": {
            "total": total_contact_messages or 0,
            "unread": unread_contact_messages or 0,
            "responded": responded_contact_messages or 0,
            "recent_7_days": recent_contact_messages or 0,
        },
        "chat_sessions": {
            "total": total_sessions or 0,
            "bot_handled": bot_handled_sessions or 0,
            "human_transferred": human_transferred_sessions or 0,
        },
        "faqs": {
            "total": total_faqs or 0,
            "active": active_faqs or 0,
        },
        "enhancements": {
            "total": total_enhancements or 0,
            "available": available_enhancements or 0,
        },
    }
