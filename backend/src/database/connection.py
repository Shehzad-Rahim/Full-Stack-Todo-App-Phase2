from sqlmodel import SQLModel, Session
from .engine import engine
from typing import Generator


def create_db_and_tables():
    """
    Create database tables based on SQLModel definitions.

    This function should be called on application startup to ensure
    all required tables exist in the database.
    """
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """
    Get a database session.

    Yields:
        Session: A SQLModel session
    """
    with Session(engine) as session:
        yield session