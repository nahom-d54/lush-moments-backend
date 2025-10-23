from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Theme
from app.schemas.theme import Theme as ThemeSchema
from app.schemas.theme import ThemeCreate
from app.utils.auth import get_current_admin

router = APIRouter(prefix="/admin/themes", tags=["admin themes"])


@router.get("/", response_model=List[ThemeSchema])
async def get_themes(
    db: AsyncSession = Depends(get_db), current_admin=Depends(get_current_admin)
):
    result = await db.execute(select(Theme))
    themes = result.scalars().all()
    return themes


@router.post("/", response_model=ThemeSchema)
async def create_theme(
    theme: ThemeCreate,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    db_theme = Theme(**theme.model_dump())
    db.add(db_theme)
    await db.commit()
    await db.refresh(db_theme)
    return db_theme


@router.get("/{theme_id}", response_model=ThemeSchema)
async def get_theme(
    theme_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    result = await db.execute(select(Theme).where(Theme.id == theme_id))
    theme = result.scalar_one_or_none()
    if not theme:
        raise HTTPException(status_code=404, detail="Theme not found")
    return theme


@router.put("/{theme_id}", response_model=ThemeSchema)
async def update_theme(
    theme_id: int,
    theme: ThemeCreate,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    result = await db.execute(select(Theme).where(Theme.id == theme_id))
    db_theme = result.scalar_one_or_none()
    if not db_theme:
        raise HTTPException(status_code=404, detail="Theme not found")

    for key, value in theme.model_dump().items():
        setattr(db_theme, key, value)

    await db.commit()
    await db.refresh(db_theme)
    return db_theme


@router.delete("/{theme_id}")
async def delete_theme(
    theme_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    result = await db.execute(select(Theme).where(Theme.id == theme_id))
    theme = result.scalar_one_or_none()
    if not theme:
        raise HTTPException(status_code=404, detail="Theme not found")

    await db.delete(theme)
    await db.commit()
    return {"message": "Theme deleted successfully"}
