from typing import Dict

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Translation


async def get_translations_for_object(
    db: AsyncSession, content_type: str, object_id: int, language_code: str = "en"
) -> Dict[str, str]:
    """
    Retrieve translations for a specific object

    Args:
        db: Database session
        content_type: Type of content (e.g., "Package", "Theme")
        object_id: ID of the object
        language_code: Language code (default: "en")

    Returns:
        Dictionary mapping field names to translated text
    """
    result = await db.execute(
        select(Translation).where(
            Translation.content_type == content_type,
            Translation.object_id == object_id,
            Translation.language_code == language_code,
        )
    )
    translations = result.scalars().all()

    return {t.field_name: t.translated_text for t in translations}


async def apply_translations(
    db: AsyncSession, obj: any, content_type: str, language_code: str = "en"
) -> any:
    """
    Apply translations to an object's fields

    Args:
        db: Database session
        obj: The object to translate
        content_type: Type of content (e.g., "Package", "Theme")
        language_code: Language code (default: "en")

    Returns:
        The object with translated fields
    """
    if language_code == "en":
        return obj  # Default language, no translation needed

    translations = await get_translations_for_object(
        db, content_type, obj.id, language_code
    )

    for field_name, translated_text in translations.items():
        if hasattr(obj, field_name):
            setattr(obj, field_name, translated_text)

    return obj
