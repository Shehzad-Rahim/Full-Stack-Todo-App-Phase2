from sqlmodel import SQLModel
from .engine import engine


def create_db_and_tables():
    """
    Create database tables based on SQLModel definitions.

    This function should be called on application startup to ensure
    all required tables exist in the database.
    """
    SQLModel.metadata.create_all(engine)