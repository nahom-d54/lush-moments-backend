from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import AuthProvider, User
from app.schemas.auth import OAuthUserInfo, Token, UserCreate
from app.schemas.auth import User as UserSchema
from app.utils.auth import create_access_token, get_password_hash, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=Token)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """Register a new user with email and password"""
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
async def login(email: str, password: str, db: AsyncSession = Depends(get_db)):
    """Login with email and password"""
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if not user or not user.password_hash:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Update last login
    user.last_login = datetime.utcnow()
    await db.commit()
    await db.refresh(user)  # Refresh to reload all attributes

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
async def oauth_callback(oauth_user: OAuthUserInfo, db: AsyncSession = Depends(get_db)):
    """
    Handle OAuth callback from frontend.
    Frontend should exchange OAuth code for user info and send it here.
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
