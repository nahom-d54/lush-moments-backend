from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class SessionBase(BaseModel):
    linked_user_id: Optional[UUID] = None


class SessionCreate(SessionBase):
    pass


class Session(SessionBase):
    session_id: str
    chat_history: Optional[str] = None

    class Config:
        from_attributes = True
