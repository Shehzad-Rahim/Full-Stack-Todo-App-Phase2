import pytest
from sqlmodel import Session, create_engine, SQLModel
from sqlmodel.pool import StaticPool
from fastapi.testclient import TestClient
from src.main import create_app


@pytest.fixture(name="session")
def session_fixture():
    """
    Create a test database session.

    This fixture creates an in-memory SQLite database for testing
    and provides a session for use in tests.
    """
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    SQLModel.metadata.create_all(bind=engine)

    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture():
    """
    Create a test client for the FastAPI app.

    This fixture creates a test client that can be used to make
    requests to the API during testing.
    """
    app = create_app()
    client = TestClient(app)
    yield client