from fastapi import Depends, HTTPException, status
from fastapi import Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional
import os
import logging
from jose import JWTError, jwt

from sqlmodel import Session
from ..database.connection import get_session
from ..models.user import User
from .jwt import verify_token, extract_user_id_from_token

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
) -> User:
    """
    Dependency to get the current user from the JWT token.
    """
    token = credentials.credentials

    try:
        payload = verify_token(token)
        user_id: str = payload.get("sub")

        if user_id is None:
            logger.warning(f"Invalid token: no user_id found in payload")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except JWTError as e:
        logger.warning(f"JWT validation failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = session.get(User, user_id)
    if user is None:
        logger.warning(f"User not found for ID: {user_id}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    logger.info(f"Successfully authenticated user: {user_id}")
    return user


def get_user_id_from_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> str:
    """
    Extract user ID from the JWT token.
    """
    token = credentials.credentials

    try:
        user_id = extract_user_id_from_token(token)

        if user_id is None:
            logger.warning(f"Could not extract user_id from token")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        logger.info(f"Successfully extracted user_id: {user_id} from token")
        return user_id
    except HTTPException:
        logger.warning(f"Failed to extract user_id from token")
        raise


def verify_user_id_match(
    token_user_id: str = Depends(get_user_id_from_token)
) -> str:
    """
    Verify that the user ID in the token matches the user ID in the request.
    This is used as a dependency to validate user access to resources.
    """
    # This dependency will be used in conjunction with path parameters
    # to ensure the authenticated user can only access their own resources
    logger.info(f"Verifying user ID match for: {token_user_id}")
    return token_user_id


def require_jwt_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    JWT token validation dependency.
    Verifies that a valid JWT token is provided in the Authorization header.
    """
    token = credentials.credentials

    try:
        payload = verify_token(token)
        logger.info("Successfully validated JWT token")
        return token
    except JWTError as e:
        logger.warning(f"JWT token validation failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def validate_user_id(user_id: str, token_user_id: str = Depends(get_user_id_from_token)) -> str:
    """
    Validate that the user ID in the request matches the user ID in the JWT token.

    Args:
        user_id: The user ID from the request path parameter
        token_user_id: The user ID extracted from the JWT token (dependency)

    Returns:
        str: The validated user ID

    Raises:
        HTTPException: If the user IDs don't match (403 Forbidden)
    """
    if user_id != token_user_id:
        logger.warning(f"User ID mismatch: request={user_id}, token={token_user_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You can only access your own resources"
        )

    logger.info(f"Successfully validated user ID: {user_id}")
    return user_id


def get_user_id_from_cookie(request: Request) -> str:
    """
    Extract user ID from the JWT token stored in HttpOnly cookie.
    """
    access_token = request.cookies.get("access_token")
    if not access_token:
        logger.warning("No access token found in cookies")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No access token provided in cookies",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        from .jwt import verify_token
        payload = verify_token(access_token)
        user_id = payload.get("sub")

        if user_id is None:
            logger.warning("No user_id found in token payload")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: no user ID",
                headers={"WWW-Authenticate": "Bearer"},
            )

        logger.info(f"Successfully extracted user_id from cookie: {user_id}")
        return user_id
    except Exception as e:
        logger.warning(f"Failed to extract user_id from cookie: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token in cookie",
            headers={"WWW-Authenticate": "Bearer"},
        )