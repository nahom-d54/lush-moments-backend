from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Testimonial
from app.schemas.testimonial import Testimonial as TestimonialSchema
from app.schemas.testimonial import TestimonialCreate
from app.utils.auth import get_current_admin

router = APIRouter(prefix="/admin/testimonials", tags=["admin testimonials"])


@router.get("/", response_model=List[TestimonialSchema])
async def get_testimonials(
    db: AsyncSession = Depends(get_db), current_admin=Depends(get_current_admin)
):
    result = await db.execute(select(Testimonial))
    testimonials = result.scalars().all()
    return testimonials


@router.post("/", response_model=TestimonialSchema)
async def create_testimonial(
    testimonial: TestimonialCreate,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    db_testimonial = Testimonial(**testimonial.model_dump())
    db.add(db_testimonial)
    await db.commit()
    await db.refresh(db_testimonial)
    return db_testimonial


@router.get("/{testimonial_id}", response_model=TestimonialSchema)
async def get_testimonial(
    testimonial_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    result = await db.execute(
        select(Testimonial).where(Testimonial.id == testimonial_id)
    )
    testimonial = result.scalar_one_or_none()
    if not testimonial:
        raise HTTPException(status_code=404, detail="Testimonial not found")
    return testimonial


@router.put("/{testimonial_id}", response_model=TestimonialSchema)
async def update_testimonial(
    testimonial_id: int,
    testimonial: TestimonialCreate,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    result = await db.execute(
        select(Testimonial).where(Testimonial.id == testimonial_id)
    )
    db_testimonial = result.scalar_one_or_none()
    if not db_testimonial:
        raise HTTPException(status_code=404, detail="Testimonial not found")

    for key, value in testimonial.model_dump().items():
        setattr(db_testimonial, key, value)

    await db.commit()
    await db.refresh(db_testimonial)
    return db_testimonial


@router.delete("/{testimonial_id}")
async def delete_testimonial(
    testimonial_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    result = await db.execute(
        select(Testimonial).where(Testimonial.id == testimonial_id)
    )
    testimonial = result.scalar_one_or_none()
    if not testimonial:
        raise HTTPException(status_code=404, detail="Testimonial not found")

    await db.delete(testimonial)
    await db.commit()
    return {"message": "Testimonial deleted successfully"}
