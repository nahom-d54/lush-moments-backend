from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Testimonial
from app.schemas.testimonial import Testimonial as TestimonialSchema

router = APIRouter()


@router.get("/testimonials", response_model=List[TestimonialSchema])
async def get_testimonials(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Testimonial))
    testimonials = result.scalars().all()
    return testimonials
