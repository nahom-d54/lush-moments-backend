import enum
from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Role(enum.Enum):
    admin = "admin"
    client = "client"


class AuthProvider(enum.Enum):
    local = "local"
    google = "google"
    github = "github"


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True, index=True, default=uuid4)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    phone: Mapped[str | None]
    password_hash: Mapped[str | None] = mapped_column(
        nullable=True
    )  # Nullable for OAuth users
    role: Mapped[Role] = mapped_column(Enum(Role), default=Role.client, nullable=False)
    auth_provider: Mapped[AuthProvider] = mapped_column(
        Enum(AuthProvider), default=AuthProvider.local, nullable=False
    )
    oauth_id: Mapped[str | None] = mapped_column(
        String(255), nullable=True, index=True
    )  # OAuth provider user ID
    avatar_url: Mapped[str | None]  # Profile picture from OAuth
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    last_login: Mapped[datetime | None]

    # Relationships
    sessions = relationship("Session", back_populates="user")
    bookings = relationship("EventBooking", back_populates="user")
