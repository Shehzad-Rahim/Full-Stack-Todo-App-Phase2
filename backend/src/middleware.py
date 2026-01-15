from fastapi import Request
from fastapi.responses import Response
import time
import logging
import re
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp, Receive, Send
from starlette.requests import Request
from starlette.responses import Response


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to log incoming requests and outgoing responses.
    """
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        # Extract method and path but mask sensitive information
        method = request.method
        path = request.url.path

        # Security monitoring: log authentication-related events
        if path.startswith('/auth'):
            logger.info(f"Authentication event: {method} {path}")

        # Log basic request info without sensitive data
        logger.info(f"Request: {method} {path}")

        response = await call_next(request)

        # Calculate response time
        process_time = time.time() - start_time

        # Add process time to response headers
        response.headers["X-Process-Time"] = str(process_time)

        # Log the response without exposing sensitive information
        status_code = response.status_code
        logger.info(f"Response: {status_code} in {process_time:.2f}s")

        # Security monitoring: log authentication failures
        if path.startswith('/auth') and status_code >= 400:
            logger.warning(f"Authentication failure: {method} {path} resulted in {status_code}")

        return response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware to add security headers to all responses.
    """
    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        # Get the request path to determine if it's a documentation endpoint
        path = request.url.path

        # Add security headers to the response
        # HTTP Strict Transport Security (HSTS)
        response.headers["strict-transport-security"] = "max-age=31536000; includeSubDomains; preload"

        # X-Content-Type-Options
        response.headers["x-content-type-options"] = "nosniff"

        # X-Frame-Options
        response.headers["x-frame-options"] = "DENY"

        # X-XSS-Protection (deprecated but still useful for older browsers)
        response.headers["x-xss-protection"] = "1; mode=block"

        # Referrer-Policy
        response.headers["referrer-policy"] = "strict-origin-when-cross-origin"

        # Content-Security-Policy - allow more resources for documentation endpoints
        if path in ["/docs", "/redoc"]:
            # Allow resources needed for Swagger UI and ReDoc
            response.headers["content-security-policy"] = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net https://unpkg.com https://cdnjs.cloudflare.com; "
                "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://fonts.googleapis.com https://unpkg.com; "
                "font-src 'self' https://fonts.gstatic.com https://cdn.jsdelivr.net; "
                "img-src 'self' data: https:; "
                "connect-src 'self'; "
                "frame-ancestors 'none';"
            )
        else:
            # More restrictive policy for API endpoints
            response.headers["content-security-policy"] = "default-src 'self'; frame-ancestors 'none';"

        # Cache-Control for API responses
        response.headers["cache-control"] = "no-store, no-cache, must-revalidate, proxy-revalidate"

        return response


