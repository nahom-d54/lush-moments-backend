from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Theme
from app.schemas.theme import Theme as ThemeSchema
from app.utils.translations import apply_translations

router = APIRouter(prefix="/themes", tags=["Themes"])


@router.get("/", response_model=List[ThemeSchema])
async def get_themes(
    db: AsyncSession = Depends(get_db),
    lang: Optional[str] = Query(
        "en", description="Language code (e.g., 'en', 'es', 'fr')"
    ),
    featured: Optional[bool] = Query(None, description="Filter by featured themes"),
    limit: Optional[int] = Query(3, description="Limit the number of themes returned"),
):
    query_term = select(Theme)
    if featured is not None:
        query_term = query_term.where(Theme.featured == featured)
    if limit is not None:
        query_term = query_term.limit(limit)
    result = await db.execute(query_term.order_by(Theme.id))
    themes = result.scalars().all()

    # Apply translations if language is not English
    if lang != "en":
        translated_themes = []
        for theme in themes:
            translated_theme = await apply_translations(db, theme, "Theme", lang)
            translated_themes.append(translated_theme)
        return translated_themes

    return themes
