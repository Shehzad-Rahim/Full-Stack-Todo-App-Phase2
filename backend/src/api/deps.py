from sqlmodel import Session
from fastapi import Depends
from ..database.engine import get_session


def get_db_session():
    """
    Get database session dependency.

    This function is used as a FastAPI dependency to provide database
    sessions to API endpoints.

    Yields:
        Session: SQLModel database session
    """
    yield next(get_session())