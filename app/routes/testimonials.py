from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Testimonial
from app.schemas.testimonial import Testimonial as TestimonialSchema

router = APIRouter(prefix="/testimonials", tags=["Testimonials"])


@router.get("/", response_model=List[TestimonialSchema])
@router.get("", response_model=List[TestimonialSchema])
async def get_testimonials(
    db: AsyncSession = Depends(get_db),
    limit: Optional[int] = Query(
        3, description="Limit the number of testimonials returned"
    ),
):
    result = await db.execute(select(Testimonial).limit(limit))
    testimonials = result.scalars().all()
    return testimonials
