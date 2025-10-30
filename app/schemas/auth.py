from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None


class UserCreate(UserBase):
    password: str
    session_id: Optional[str] = None


class LoginRequest(BaseModel):
    """Login request with email and password"""

    email: EmailStr
    password: str
    session_id: Optional[str] = None


class User(UserBase):
    id: UUID
    role: str
    auth_provider: str
    avatar_url: Optional[str] = None

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
    user: Optional[User] = None  # Include user info in token response


class TokenData(BaseModel):
    username: Optional[str] = None


class OAuthCallback(BaseModel):
    """OAuth callback data from frontend"""

    code: str
    state: Optional[str] = None


class OAuthUserInfo(BaseModel):
    """User information from OAuth provider"""

    provider: str  # 'google' or 'github'
    oauth_id: str  # Provider's user ID
    email: EmailStr
    name: str
    avatar_url: Optional[str] = None
    session_id: Optional[str] = None
