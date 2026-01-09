from fastapi import Request
from fastapi.responses import Response
import time
import logging


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RequestLoggingMiddleware:
    """
    Middleware to log incoming requests and outgoing responses.
    """
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        request = Request(scope)
        start_time = time.time()

        # Log the incoming request
        logger.info(f"Request: {request.method} {request.url.path}")

        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                # Calculate response time
                process_time = time.time() - start_time
                response_headers = dict(message.get("headers", []))

                # Add process time to response headers
                response_headers[b"X-Process-Time"] = str(process_time).encode("latin-1")
                message["headers"] = [(k, v) for k, v in response_headers.items()]

                # Log the response
                status_code = message["status"]
                logger.info(f"Response: {status_code} in {process_time:.2f}s")

            await send(message)

        return await self.app(scope, receive, send)


def add_logging_middleware(app):
    """
    Add request logging middleware to the FastAPI app.

    Args:
        app: FastAPI application instance
    """
    app.middleware("http")(RequestLoggingMiddleware)