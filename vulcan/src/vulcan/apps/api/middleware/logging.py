"""
Logging middleware for the Vulcan API.
"""
import logging
import time
import uuid
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from vulcan.apps.api.config import LOG_LEVEL


# Configure logger
logger = logging.getLogger("vulcan-api")
logger.setLevel(getattr(logging, LOG_LEVEL))


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging requests and responses."""
    
    def __init__(self, app: ASGIApp):
        """
        Initialize the middleware.
        
        Args:
            app: ASGI application
        """
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process the request and log information.
        
        Args:
            request: HTTP request
            call_next: Next middleware in the chain
            
        Returns:
            HTTP response
        """
        # Generate request ID
        request_id = str(uuid.uuid4())
        
        # Add request ID to request state
        request.state.request_id = request_id
        
        # Log request
        logger.info(
            f"Request {request_id}: {request.method} {request.url.path} "
            f"from {request.client.host if request.client else 'unknown'}"
        )
        
        # Process request and measure time
        start_time = time.time()
        
        try:
            response = await call_next(request)
            
            # Calculate processing time
            process_time = time.time() - start_time
            
            # Log response
            logger.info(
                f"Response {request_id}: {response.status_code} "
                f"processed in {process_time:.4f}s"
            )
            
            # Add custom headers
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Process-Time"] = str(process_time)
            
            return response
        
        except Exception as e:
            # Log exception
            logger.error(
                f"Error {request_id}: {str(e)} "
                f"occurred after {time.time() - start_time:.4f}s"
            )
            raise