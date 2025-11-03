from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import AuthProvider, User
from app.schemas.auth import (
    AnonymousLoginResponse,
    LoginRequest,
    OAuthUserInfo,
    Token,
    UserCreate,
)
from app.schemas.auth import User as UserSchema
from app.utils.auth import (
    create_access_token,
    get_current_user_optional,
    get_password_hash,
    verify_password,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/anonymous", response_model=AnonymousLoginResponse)
async def create_anonymous_user(db: AsyncSession = Depends(get_db)):
    """
    Create an anonymous user account for chat access.
    This allows users to use the chat feature without full registration.
    """
    # Create anonymous user
    anonymous_email = f"anonymous_{uuid4()}@lushmoments.temp"
    db_user = User(
        name=f"Guest_{uuid4().hex[:8]}",
        email=anonymous_email,
        password_hash=None,
        auth_provider=AuthProvider.local,
        isAnonymous=True,
        last_login=datetime.utcnow(),
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    # Create access token
    access_token = create_access_token(
        data={"sub": db_user.id.hex, "isAnonymous": True},
        expires_delta=timedelta(days=30),
    )

    return AnonymousLoginResponse(
        access_token=access_token,
        token_type="bearer",
        user_id=db_user.id,
        is_anonymous=True,
    )


async def convert_anonymous_to_regular(
    db: AsyncSession,
    anonymous_user: User,
    name: str,
    email: str,
    phone: Optional[str],
    password_hash: Optional[str] = None,
) -> User:
    """
    Helper function to convert an anonymous user account to a regular account.
    """
    # Check if email is already taken by a non-anonymous user
    result = await db.execute(
        select(User).where(User.email == email, ~User.isAnonymous)
    )
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Update the anonymous user to a regular user
    anonymous_user.name = name
    anonymous_user.email = email
    anonymous_user.phone = phone
    anonymous_user.password_hash = password_hash
    anonymous_user.isAnonymous = False
    anonymous_user.last_login = datetime.utcnow()

    await db.commit()
    await db.refresh(anonymous_user)

    return anonymous_user


@router.post("/register", response_model=Token)
async def register(
    user: UserCreate,
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional),
):
    """
    Register a new user with email and password.
    If the current user is anonymous, convert their account to a regular account.
    Otherwise, create a new account.
    """
    # If user is already logged in as anonymous, convert the account
    if current_user and current_user.isAnonymous:
        hashed_password = get_password_hash(user.password)
        db_user = await convert_anonymous_to_regular(
            db, current_user, user.name, user.email, user.phone, hashed_password
        )
    else:
        # Check if user exists
        result = await db.execute(select(User).where(User.email == user.email))
        existing_user = result.scalar_one_or_none()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        # Create new user
        hashed_password = get_password_hash(user.password)
        db_user = User(
            name=user.name,
            email=user.email,
            phone=user.phone,
            password_hash=hashed_password,
            auth_provider=AuthProvider.local,
            isAnonymous=False,
            last_login=datetime.utcnow(),
        )
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)

    # Create token
    access_token = create_access_token(
        data={"sub": db_user.id.hex, "isAnonymous": False}
    )

    return Token(
        access_token=access_token,
        token_type="bearer",
        user=UserSchema(
            id=db_user.id,
            name=db_user.name,
            email=db_user.email,
            phone=db_user.phone,
            role=db_user.role.value,
            auth_provider=db_user.auth_provider.value,
            avatar_url=db_user.avatar_url,
        ),
    )


@router.post("/login", response_model=Token)
async def login(
    user_request: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Login with email and password.
    """
    result = await db.execute(select(User).where(User.email == user_request.email))
    user = result.scalar_one_or_none()

    if not user or not user.password_hash:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(user_request.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Don't allow login to anonymous accounts
    if user.isAnonymous:
        raise HTTPException(
            status_code=400,
            detail="This is an anonymous account. Please register with your email and password.",
        )

    # Update last login
    user.last_login = datetime.utcnow()
    await db.commit()
    await db.refresh(user)

    access_token = create_access_token(data={"sub": user.id.hex, "isAnonymous": False})

    return Token(
        access_token=access_token,
        token_type="bearer",
        user=UserSchema(
            id=user.id,
            name=user.name,
            email=user.email,
            phone=user.phone,
            role=user.role.value,
            auth_provider=user.auth_provider.value,
            avatar_url=user.avatar_url,
        ),
    )


@router.post("/oauth/callback", response_model=Token)
async def oauth_callback(
    oauth_user: OAuthUserInfo,
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional),
):
    """
    Handle OAuth callback from frontend.
    Frontend should exchange OAuth code for user info and send it here.
    If the current user is anonymous, convert their account to OAuth account.
    """
    # If user is already logged in as anonymous, convert the account
    if current_user and current_user.isAnonymous:
        user = await convert_anonymous_to_regular(
            db,
            current_user,
            oauth_user.name,
            oauth_user.email,
            None,  # OAuth users typically don't have phone
            None,  # No password for OAuth users
        )
        # Update OAuth-specific fields
        user.auth_provider = AuthProvider[oauth_user.provider]
        user.oauth_id = oauth_user.oauth_id
        user.avatar_url = oauth_user.avatar_url
        await db.commit()
        await db.refresh(user)
    else:
        # Check if user exists by OAuth ID
        result = await db.execute(
            select(User).where(
                User.oauth_id == oauth_user.oauth_id,
                User.auth_provider == AuthProvider[oauth_user.provider],
            )
        )
        user = result.scalar_one_or_none()

        if not user:
            # Check if email is already registered with different provider
            result = await db.execute(
                select(User).where(User.email == oauth_user.email)
            )
            existing_user = result.scalar_one_or_none()

            if existing_user:
                raise HTTPException(
                    status_code=400,
                    detail=f"Email already registered with {existing_user.auth_provider.value} provider",
                )

            # Create new user
            user = User(
                name=oauth_user.name,
                email=oauth_user.email,
                auth_provider=AuthProvider[oauth_user.provider],
                oauth_id=oauth_user.oauth_id,
                avatar_url=oauth_user.avatar_url,
                password_hash=None,  # No password for OAuth users
                isAnonymous=False,
                last_login=datetime.now(timezone.utc),
            )
            db.add(user)
            await db.commit()
            await db.refresh(user)
        else:
            # Update existing user info
            user.name = oauth_user.name
            user.avatar_url = oauth_user.avatar_url
            user.last_login = datetime.now(timezone.utc)
            await db.commit()

    # Create token
    access_token = create_access_token(data={"sub": user.id.hex, "isAnonymous": False})

    return Token(
        access_token=access_token,
        token_type="bearer",
        user=UserSchema(
            id=user.id,
            name=user.name,
            email=user.email,
            phone=user.phone,
            role=user.role.value,
            auth_provider=user.auth_provider.value,
            avatar_url=user.avatar_url,
        ),
    )
