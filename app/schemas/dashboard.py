from pydantic import BaseModel, Field


class BookingStatusStats(BaseModel):
    """Statistics breakdown by booking status"""

    pending: int = Field(ge=0, description="Number of pending bookings")
    confirmed: int = Field(ge=0, description="Number of confirmed bookings")
    completed: int = Field(ge=0, description="Number of completed bookings")
    cancelled: int = Field(ge=0, description="Number of cancelled bookings")


class BookingsStats(BaseModel):
    """Bookings statistics"""

    total: int = Field(ge=0, description="Total number of bookings")
    by_status: BookingStatusStats = Field(description="Breakdown by booking status")
    recent_30_days: int = Field(
        ge=0, description="Number of bookings created in the last 30 days"
    )


class UsersStats(BaseModel):
    """Users statistics"""

    total: int = Field(ge=0, description="Total number of users")
    admins: int = Field(ge=0, description="Number of admin users")
    clients: int = Field(ge=0, description="Number of client users")
    anonymous: int = Field(ge=0, description="Number of anonymous users")


class PackagesStats(BaseModel):
    """Packages statistics"""

    total: int = Field(ge=0, description="Total number of packages")


class ThemesStats(BaseModel):
    """Themes statistics"""

    total: int = Field(ge=0, description="Total number of themes")
    featured: int = Field(ge=0, description="Number of featured themes")


class GalleryStats(BaseModel):
    """Gallery statistics"""

    total_items: int = Field(ge=0, description="Total number of gallery items")
    featured_items: int = Field(ge=0, description="Number of featured gallery items")
    total_categories: int = Field(
        ge=0, description="Total number of gallery categories"
    )
    active_categories: int = Field(
        ge=0, description="Number of active gallery categories"
    )


class TestimonialsStats(BaseModel):
    """Testimonials statistics"""

    total: int = Field(ge=0, description="Total number of testimonials")


class ContactMessagesStats(BaseModel):
    """Contact messages statistics"""

    total: int = Field(ge=0, description="Total number of contact messages")
    unread: int = Field(ge=0, description="Number of unread messages")
    responded: int = Field(ge=0, description="Number of responded messages")
    recent_7_days: int = Field(
        ge=0, description="Number of messages received in the last 7 days"
    )


class ChatSessionsStats(BaseModel):
    """Chat sessions statistics"""

    total: int = Field(ge=0, description="Total number of chat sessions")
    bot_handled: int = Field(ge=0, description="Number of sessions handled by bot")
    human_transferred: int = Field(
        ge=0, description="Number of sessions transferred to human"
    )


class FAQsStats(BaseModel):
    """FAQs statistics"""

    total: int = Field(ge=0, description="Total number of FAQs")
    active: int = Field(ge=0, description="Number of active FAQs")


class EnhancementsStats(BaseModel):
    """Package enhancements statistics"""

    total: int = Field(ge=0, description="Total number of enhancements")
    available: int = Field(ge=0, description="Number of available enhancements")


class DashboardStatsResponse(BaseModel):
    """Comprehensive dashboard statistics response"""

    bookings: BookingsStats = Field(description="Bookings statistics")
    users: UsersStats = Field(description="Users statistics")
    packages: PackagesStats = Field(description="Packages statistics")
    themes: ThemesStats = Field(description="Themes statistics")
    gallery: GalleryStats = Field(description="Gallery statistics")
    testimonials: TestimonialsStats = Field(description="Testimonials statistics")
    contact_messages: ContactMessagesStats = Field(
        description="Contact messages statistics"
    )
    chat_sessions: ChatSessionsStats = Field(description="Chat sessions statistics")
    faqs: FAQsStats = Field(description="FAQs statistics")
    enhancements: EnhancementsStats = Field(
        description="Package enhancements statistics"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "bookings": {
                    "total": 25,
                    "by_status": {
                        "pending": 5,
                        "confirmed": 10,
                        "completed": 8,
                        "cancelled": 2,
                    },
                    "recent_30_days": 12,
                },
                "users": {"total": 150, "admins": 2, "clients": 140, "anonymous": 8},
                "packages": {"total": 5},
                "themes": {"total": 10, "featured": 3},
                "gallery": {
                    "total_items": 45,
                    "featured_items": 5,
                    "total_categories": 6,
                    "active_categories": 5,
                },
                "testimonials": {"total": 15},
                "contact_messages": {
                    "total": 30,
                    "unread": 5,
                    "responded": 20,
                    "recent_7_days": 8,
                },
                "chat_sessions": {
                    "total": 100,
                    "bot_handled": 95,
                    "human_transferred": 5,
                },
                "faqs": {"total": 20, "active": 18},
                "enhancements": {"total": 12, "available": 10},
            }
        }
