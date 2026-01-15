from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Response, Request
from datetime import timedelta
from typing import Dict
from sqlmodel import Session, select
from slowapi import Limiter
from slowapi.util import get_remote_address

from ...models.user import User, UserCreate
from ...database.connection import get_session
from ...auth.utils import verify_password, get_password_hash, validate_email, validate_password_strength
from ...auth.jwt import create_access_token, create_refresh_token, refresh_access_token
from ...config import settings

# Security for refresh endpoint
security = HTTPBearer()

# Initialize rate limiter for auth endpoints
limiter = Limiter(key_func=get_remote_address)

router = APIRouter()




@router.post("/auth/signup", response_model=Dict[str, str])
# @limiter.limit("5/minute")  # Rate limit signup attempts
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

    # Create access and refresh tokens
    access_token = create_access_token(
        data={"sub": user.id, "email": user.email}
    )
    refresh_token = create_refresh_token(
        data={"sub": user.id, "email": user.email}
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user_id": user.id,
        "email": user.email
    }


@router.post("/auth/signin", response_model=Dict[str, str])
# @limiter.limit("10/minute")  # Rate limit sign in attempts
def signin(request: Request, response: Response, user_create: UserCreate, session: Session = Depends(get_session)):
    """
    Authenticate user and return JWT tokens.
    """
    # Find user by email
    user = session.exec(select(User).where(User.email == user_create.email)).first()
    if not user or not verify_password(user_create.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access and refresh tokens
    access_token = create_access_token(
        data={"sub": user.id, "email": user.email}
    )
    refresh_token = create_refresh_token(
        data={"sub": user.id, "email": user.email}
    )
    
    # Set HttpOnly cookies for frontend
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,  # True if using HTTPS in production
        samesite="lax",
        max_age=900,  # 15 minutes
        path="/"
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,  # True if using HTTPS
        samesite="lax",
        max_age=604800,  # 7 days
        path="/"
    )


    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user_id": user.id,
        "email": user.email
    }


@router.post("/auth/refresh", response_model=Dict[str, str])
# @limiter.limit("5/minute")  # Rate limit refresh attempts
def refresh_token_endpoint(request: Request, response: Response, credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Refresh an access token using a refresh token.
    """
    refresh_token_str = credentials.credentials

    new_access_token, new_refresh_token = refresh_access_token(refresh_token_str)

    response.set_cookie(
        key="access_token",
        value=new_access_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=900,  # 15 minutes
        path="/"
    )

    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=604800,  # 7 days
        path="/"
    )

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }


@router.get("/auth/me")
def get_current_user(request: Request, session: Session = Depends(get_session)):
    """
    Get current authenticated user's information.
    """
    # Get tokens from cookies
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No access token provided",
            headers={"WWW-Authenticate": "Bearer"},
        )

    from ...auth.jwt import verify_token
    try:
        payload = verify_token(access_token)
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: no user ID",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Fetch user from database
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Return user information (excluding password hash)
    return {
        "id": user.id,
        "email": user.email,
        "created_at": user.created_at.isoformat() if user.created_at else None,
        "updated_at": user.updated_at.isoformat() if user.updated_at else None,
    }


@router.post("/auth/logout")
def logout(response: Response):
    """
    Clear authentication cookies to log out user.
    """
    # Clear the HttpOnly cookies
    response.set_cookie(
        key="access_token",
        value="",
        httponly=True,
        secure=False,  # True if using HTTPS in production
        samesite="lax",
        max_age=0,  # Expire immediately
        path="/"
    )

    response.set_cookie(
        key="refresh_token",
        value="",
        httponly=True,
        secure=False,  # True if using HTTPS
        samesite="lax",
        max_age=0,  # Expire immediately
        path="/"
    )

    return {"message": "Successfully logged out"}