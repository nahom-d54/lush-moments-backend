from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Translation
from app.schemas.translation import Translation as TranslationSchema
from app.schemas.translation import TranslationCreate
from app.utils.auth import get_current_admin

router = APIRouter(prefix="/admin/translations", tags=["admin translations"])


@router.get("/", response_model=List[TranslationSchema])
@router.get("", response_model=List[TranslationSchema])
async def get_translations(
    db: AsyncSession = Depends(get_db), current_admin=Depends(get_current_admin)
):
    result = await db.execute(select(Translation))
    translations = result.scalars().all()
    return translations


@router.post("/", response_model=TranslationSchema)
async def create_translation(
    translation: TranslationCreate,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    db_translation = Translation(**translation.model_dump())
    db.add(db_translation)
    await db.commit()
    await db.refresh(db_translation)
    return db_translation


@router.get("/{translation_id}", response_model=TranslationSchema)
@router.get("/{translation_id}/", response_model=TranslationSchema)
async def get_translation(
    translation_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    result = await db.execute(
        select(Translation).where(Translation.id == translation_id)
    )
    translation = result.scalar_one_or_none()
    if not translation:
        raise HTTPException(status_code=404, detail="Translation not found")
    return translation


@router.put("/{translation_id}", response_model=TranslationSchema)
@router.put("/{translation_id}/", response_model=TranslationSchema)
async def update_translation(
    translation_id: int,
    translation: TranslationCreate,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    result = await db.execute(
        select(Translation).where(Translation.id == translation_id)
    )
    db_translation = result.scalar_one_or_none()
    if not db_translation:
        raise HTTPException(status_code=404, detail="Translation not found")

    for key, value in translation.model_dump().items():
        setattr(db_translation, key, value)

    await db.commit()
    await db.refresh(db_translation)
    return db_translation


@router.delete("/{translation_id}")
@router.delete("/{translation_id}/")
async def delete_translation(
    translation_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    result = await db.execute(
        select(Translation).where(Translation.id == translation_id)
    )
    translation = result.scalar_one_or_none()
    if not translation:
        raise HTTPException(status_code=404, detail="Translation not found")

    await db.delete(translation)
    await db.commit()
    return {"message": "Translation deleted successfully"}
