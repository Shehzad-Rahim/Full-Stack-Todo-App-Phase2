from sqlalchemy import create_engine
from sqlmodel import Session
from typing import Generator
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_backend.db")

# For testing purposes, we might need different engine options
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False

engine = create_engine(
    DATABASE_URL,
    echo=False,  # Set to True for SQL query logging
    connect_args=connect_args
)


def get_session() -> Generator[Session, None, None]:
    """
    Get a database session.

    Yields:
        Session: A SQLModel session
    """
    with Session(engine) as session:
        yield session