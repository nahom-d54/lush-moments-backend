import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Session as SessionModel
from app.schemas.session import Session, SessionCreate

router = APIRouter()


@router.post("/sessions", response_model=Session)
async def create_session(session: SessionCreate, db: AsyncSession = Depends(get_db)):
    session_id = str(uuid.uuid4())
    db_session = SessionModel(
        session_id=session_id, linked_user_id=session.linked_user_id
    )
    db.add(db_session)
    await db.commit()
    await db.refresh(db_session)
    return db_session
