from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Session
from app.models.user import AuthProvider, User
from app.schemas.auth import LoginRequest, OAuthUserInfo, Token, UserCreate
from app.schemas.auth import User as UserSchema
from app.utils.auth import create_access_token, get_password_hash, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])


async def merge_anonymous_session(
    db: AsyncSession, user_id: str, session_id: Optional[str]
) -> None:
    """
    Helper function to merge an anonymous chat session with a user account.
    Called after successful login/registration.
    """
    if not session_id:
        return

    try:
        # Get the anonymous session
        result = await db.execute(
            select(Session).where(Session.session_id == session_id)
        )
        anonymous_session = result.scalar_one_or_none()

        if not anonymous_session:
            # Create a new session linked to the user
            new_session = Session(session_id=session_id, linked_user_id=user_id)
            db.add(new_session)
            await db.commit()
            return

        # If session is already linked to this user, nothing to do
        if anonymous_session.linked_user_id == user_id:
            return

        # If session is not linked to any user, link it to this user
        if anonymous_session.linked_user_id is None:
            anonymous_session.linked_user_id = user_id
            await db.commit()
            return

        # If session is linked to a different user, we don't merge
        # to prevent session hijacking
        return

    except Exception as e:
        # Log the error but don't fail the auth process
        print(f"Failed to merge session {session_id}: {e}")
        return


@router.post("/register", response_model=Token)
async def register(
    user: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    Register a new user with email and password.
    Optionally provide session_id in request body to merge anonymous chat session.
    """
    # Check if user exists
    result = await db.execute(select(User).where(User.email == user.email))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create user
    hashed_password = get_password_hash(user.password)
    db_user = User(
        name=user.name,
        email=user.email,
        phone=user.phone,
        password_hash=hashed_password,
        auth_provider=AuthProvider.local,
        last_login=datetime.utcnow(),
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    # Merge anonymous chat session if provided
    await merge_anonymous_session(db, db_user.id, user.session_id)

    # Create token
    access_token = create_access_token(data={"sub": db_user.email})

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
    Optionally provide session_id to merge anonymous chat session.
    """
    result = await db.execute(select(User).where(User.email == user_request.email))
    user = result.scalar_one_or_none()

    if not user or not user.password_hash:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(user_request.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Update last login
    user.last_login = datetime.utcnow()
    await db.commit()
    await db.refresh(user)  # Refresh to reload all attributes

    # Merge anonymous chat session if provided
    await merge_anonymous_session(db, user.id, user_request.session_id)

    access_token = create_access_token(data={"sub": user.email})

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
    session_id: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """
    Handle OAuth callback from frontend.
    Frontend should exchange OAuth code for user info and send it here.
    Optionally provide session_id to merge anonymous chat session.
    """
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
        result = await db.execute(select(User).where(User.email == oauth_user.email))
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
            last_login=datetime.utcnow(),
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
    else:
        # Update existing user info
        user.name = oauth_user.name
        user.avatar_url = oauth_user.avatar_url
        user.last_login = datetime.utcnow()
        await db.commit()

    # Merge anonymous chat session if provided
    await merge_anonymous_session(db, user.id, session_id)

    # Create token
    access_token = create_access_token(data={"sub": user.email})

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
