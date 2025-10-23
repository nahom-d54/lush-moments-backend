from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Session
from app.schemas.session import Session as SessionSchema
from app.schemas.session import SessionCreate
from app.utils.auth import get_current_admin

router = APIRouter(prefix="/admin/sessions", tags=["admin sessions"])


@router.get("/", response_model=List[SessionSchema])
async def get_sessions(
    db: AsyncSession = Depends(get_db), current_admin=Depends(get_current_admin)
):
    result = await db.execute(select(Session))
    sessions = result.scalars().all()
    return sessions


@router.post("/", response_model=SessionSchema)
async def create_session(
    session: SessionCreate,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    db_session = Session(**session.model_dump())
    db.add(db_session)
    await db.commit()
    await db.refresh(db_session)
    return db_session


@router.get("/{session_id}", response_model=SessionSchema)
async def get_session(
    session_id: str,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    result = await db.execute(select(Session).where(Session.session_id == session_id))
    session = result.scalar_one_or_none()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@router.put("/{session_id}", response_model=SessionSchema)
async def update_session(
    session_id: str,
    session: SessionCreate,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    result = await db.execute(select(Session).where(Session.session_id == session_id))
    db_session = result.scalar_one_or_none()
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")

    for key, value in session.model_dump().items():
        setattr(db_session, key, value)

    await db.commit()
    await db.refresh(db_session)
    return db_session


@router.delete("/{session_id}")
async def delete_session(
    session_id: str,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    result = await db.execute(select(Session).where(Session.session_id == session_id))
    session = result.scalar_one_or_none()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    await db.delete(session)
    await db.commit()
    return {"message": "Session deleted successfully"}
