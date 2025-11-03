from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

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
    category: Optional[str] = Query(
        None, description="Filter by category slug or name"
    ),
    limit: Optional[int] = Query(3, description="Limit the number of themes returned"),
):
    query_term = select(Theme).options(selectinload(Theme.category))

    if featured is not None:
        query_term = query_term.where(Theme.featured == featured)

    if category:
        # Join with category to filter by slug or name
        from app.models.gallery_category import GalleryCategory

        cat_result = await db.execute(
            select(GalleryCategory).where(
                (GalleryCategory.slug == category) | (GalleryCategory.name == category)
            )
        )
        cat_obj = cat_result.scalar_one_or_none()
        if cat_obj:
            query_term = query_term.where(Theme.category_id == cat_obj.id)

    if limit is not None:
        query_term = query_term.limit(limit)

    result = await db.execute(query_term.order_by(Theme.id))
    themes = result.scalars().all()

    # Convert to response format with category name
    themes_with_category = []
    for theme in themes:
        # Apply translations if language is not English
        if lang != "en":
            theme = await apply_translations(db, theme, "Theme", lang)

        theme_dict = ThemeSchema.model_validate(theme).model_dump()
        theme_dict["category_name"] = theme.category.name if theme.category else None
        themes_with_category.append(ThemeSchema(**theme_dict))

    return themes_with_category
