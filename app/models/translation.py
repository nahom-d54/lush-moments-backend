from uuid import UUID, uuid4

from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Translation(Base):
    __tablename__ = "translations"

    id: Mapped[UUID] = mapped_column(primary_key=True, index=True, default=uuid4)
    content_type: Mapped[str] = mapped_column(
        nullable=False
    )  # e.g., "Package", "Theme"
    object_id: Mapped[int] = mapped_column(
        nullable=False
    )  # ID of the object being translated
    language_code: Mapped[str] = mapped_column(nullable=False)  # e.g., "en", "es"
    field_name: Mapped[str] = mapped_column(
        nullable=False
    )  # e.g., "name", "description"
    translated_text: Mapped[str] = mapped_column(Text, nullable=False)
