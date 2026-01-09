from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Request
from datetime import timedelta
from typing import Dict
from sqlmodel import Session, select
from slowapi import Limiter
from slowapi.util import get_remote_address

from ...models.user import User, UserCreate
from ...database.connection import get_session
from ...auth.utils import verify_password, get_password_hash, validate_email, validate_password_strength
from ...auth.jwt import create_access_token
from ...config import settings

# Security for refresh endpoint
security = HTTPBearer()

# Initialize rate limiter for auth endpoints
limiter = Limiter(key_func=get_remote_address)

router = APIRouter()


@router.post("/auth/signup", response_model=Dict[str, str])
@limiter.limit("5/minute")  # Rate limit signup attempts
def signup(request: Request, user_create: UserCreate, session: Session = Depends(get_session)):
    """
    Create a new user account.
    """
    # Validate email format
    if not validate_email(user_create.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format"
        )

    # Validate password strength
    if not validate_password_strength(user_create.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters long"
        )

    # Check if user with this email already exists
    existing_user = session.exec(select(User).where(User.email == user_create.email)).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )

    # Hash the password
    password_hash = get_password_hash(user_create.password)

    # Create new user
    user = User(
        email=user_create.email,
        password_hash=password_hash
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    # Create access token
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.id, "email": user.email},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "email": user.email
    }


@router.post("/auth/signin", response_model=Dict[str, str])
@limiter.limit("10/minute")  # Rate limit sign in attempts
def signin(request: Request, user_create: UserCreate, session: Session = Depends(get_session)):
    """
    Authenticate user and return JWT token.
    """
    # Find user by email
    user = session.exec(select(User).where(User.email == user_create.email)).first()
    if not user or not verify_password(user_create.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.id, "email": user.email},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "email": user.email
    }


@router.post("/auth/refresh", response_model=Dict[str, str])
@limiter.limit("5/minute")  # Rate limit refresh attempts
def refresh_token(request: Request, credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Refresh an access token.
    """
    token = credentials.credentials

    from ...auth.jwt import refresh_access_token
    new_token = refresh_access_token(token)

    return {
        "access_token": new_token,
        "token_type": "bearer"
    }