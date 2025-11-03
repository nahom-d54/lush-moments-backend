from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[UUID] = mapped_column(primary_key=True, index=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        unique=True,  # One-to-one relationship
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Agent/Human handoff fields
    is_handled_by_agent: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False
    )
    transferred_to_human: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    transfer_reason: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationships
    user = relationship("User", back_populates="session", uselist=False)
    messages = relationship(
        "ChatMessage", back_populates="session", cascade="all, delete-orphan"
    )
