from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from starlette.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from pydantic import ValidationError
from .database.connection import create_db_and_tables
from .api.routes import tasks, auth
from .config import settings
from .middleware import RequestLoggingMiddleware, SecurityHeadersMiddleware
import uvicorn
import logging


# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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

    # Add rate limiting
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    # Add logging middleware
    from .middleware import RequestLoggingMiddleware, SecurityHeadersMiddleware
    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(SecurityHeadersMiddleware)

    # Create database tables on startup
    @app.on_event("startup")
    def on_startup():
        create_db_and_tables()

    # Include API routes
    app.include_router(tasks.router, tags=["tasks"])
    app.include_router(auth.router, tags=["auth"])  # Include auth routes

    @app.get("/")
    def read_root():
        return {"message": "Welcome to the Todo Backend API"}

    # Exception handlers for authentication errors
    @app.exception_handler(RateLimitExceeded)
    async def rate_limit_handler(request, exc):
        logger.warning(f"Rate limit exceeded for IP: {get_remote_address(request.scope)}")
        return JSONResponse(
            status_code=429,
            content={"detail": "Rate limit exceeded"}
        )

    # Global exception handler
    @app.exception_handler(500)
    async def global_exception_handler(request, exc):
        logger.error(f"Internal server error: {str(exc)}")
        return {"message": "An internal server error occurred", "error": str(exc)}

    # Handle validation errors
    @app.exception_handler(ValidationError)
    async def validation_exception_handler(request, exc):
        logger.warning(f"Validation error: {exc}")
        return JSONResponse(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": exc.errors()}
        )

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