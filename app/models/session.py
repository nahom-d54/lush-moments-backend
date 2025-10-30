from datetime import datetime
from uuid import UUID

from sqlalchemy import Boolean, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Session(Base):
    __tablename__ = "sessions"

    session_id: Mapped[str] = mapped_column(primary_key=True, index=True)
    linked_user_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    chat_history: Mapped[str | None] = mapped_column(
        Text
    )  # JSON string of chat messages

    # Agent/Human handoff fields
    is_handled_by_agent: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False
    )
    transferred_to_human: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    transfer_reason: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationships
    user = relationship("User", back_populates="sessions")
    messages = relationship("ChatMessage", back_populates="session")
