from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database.connection import create_db_and_tables
from .api.routes import tasks
from .config import settings
from .middleware import add_logging_middleware
import uvicorn


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        FastAPI: Configured application instance
    """
    app = FastAPI(
        title="Todo Backend API",
        description="RESTful API for managing tasks with user-based data isolation",
        version="0.1.0",
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, restrict this to your frontend domains
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add logging middleware
    add_logging_middleware(app)

    # Create database tables on startup
    @app.on_event("startup")
    def on_startup():
        create_db_and_tables()

    # Include API routes
    app.include_router(tasks.router, prefix="/api/{user_id}", tags=["tasks"])

    @app.get("/")
    def read_root():
        return {"message": "Welcome to the Todo Backend API"}

    # Global exception handler
    @app.exception_handler(500)
    async def global_exception_handler(request, exc):
        return {"message": "An internal server error occurred", "error": str(exc)}

    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level=settings.log_level
    )