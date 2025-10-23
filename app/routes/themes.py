from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Theme
from app.schemas.theme import Theme as ThemeSchema
from app.utils.translations import apply_translations

router = APIRouter()


@router.get("/themes", response_model=List[ThemeSchema])
async def get_themes(
    db: AsyncSession = Depends(get_db),
    lang: Optional[str] = Query(
        "en", description="Language code (e.g., 'en', 'es', 'fr')"
    ),
):
    result = await db.execute(select(Theme))
    themes = result.scalars().all()

    # Apply translations if language is not English
    if lang != "en":
        translated_themes = []
        for theme in themes:
            translated_theme = await apply_translations(db, theme, "Theme", lang)
            translated_themes.append(translated_theme)
        return translated_themes

    return themes
