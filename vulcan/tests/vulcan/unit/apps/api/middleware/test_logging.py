"""
Unit tests for the Vulcan API logging middleware.
"""
import logging
import time
import uuid
from unittest.mock import patch, MagicMock, AsyncMock

import pytest
from starlette.middleware.base import BaseHTTPMiddleware

from vulcan.apps.api.middleware.logging import LoggingMiddleware, logger


def test_logging_middleware_initialization():
    """Test that the LoggingMiddleware is initialized correctly."""
    # Create a mock app
    mock_app = MagicMock()
    
    # Initialize the middleware
    middleware = LoggingMiddleware(mock_app)
    
    # Assert that the middleware is a BaseHTTPMiddleware
    assert isinstance(middleware, BaseHTTPMiddleware)
    
    # Assert that the app is set correctly
    assert middleware.app == mock_app


@pytest.mark.asyncio
@patch("vulcan.apps.api.middleware.logging.uuid.uuid4")
@patch("vulcan.apps.api.middleware.logging.time.time")
@patch("vulcan.apps.api.middleware.logging.logger")
async def test_dispatch_success(mock_logger, mock_time, mock_uuid4):
    """Test that the dispatch method logs requests and responses correctly."""
    # Set up mocks
    mock_uuid4.return_value = uuid.UUID("12345678-1234-5678-1234-567812345678")
    mock_time.side_effect = [100.0, 100.5]  # Start time, end time
    
    # Create a mock request
    mock_request = MagicMock()
    mock_request.method = "GET"
    mock_request.url.path = "/api/v1/test"
    mock_request.client.host = "127.0.0.1"
    mock_request.state = MagicMock()
    
    # Create a mock response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.headers = {}
    
    # Create a mock call_next function
    mock_call_next = AsyncMock(return_value=mock_response)
    
    # Create a mock app
    mock_app = MagicMock()
    
    # Initialize the middleware
    middleware = LoggingMiddleware(mock_app)
    
    # Call dispatch
    response = await middleware.dispatch(mock_request, mock_call_next)
    
    # Assert that the request ID was set on the request state
    assert mock_request.state.request_id == "12345678-1234-5678-1234-567812345678"
    
    # Assert that the request was logged
    mock_logger.info.assert_any_call(
        "Request 12345678-1234-5678-1234-567812345678: GET /api/v1/test from 127.0.0.1"
    )
    
    # Assert that call_next was called with the request
    mock_call_next.assert_called_once_with(mock_request)
    
    # Assert that the response was logged
    mock_logger.info.assert_any_call(
        "Response 12345678-1234-5678-1234-567812345678: 200 processed in 0.5000s"
    )
    
    # Assert that the response headers were set
    assert response.headers["X-Request-ID"] == "12345678-1234-5678-1234-567812345678"
    assert response.headers["X-Process-Time"] == "0.5"
    
    # Assert that the response was returned
    assert response == mock_response


@pytest.mark.asyncio
@patch("vulcan.apps.api.middleware.logging.uuid.uuid4")
@patch("vulcan.apps.api.middleware.logging.time.time")
@patch("vulcan.apps.api.middleware.logging.logger")
async def test_dispatch_exception(mock_logger, mock_time, mock_uuid4):
    """Test that the dispatch method logs exceptions correctly."""
    # Set up mocks
    mock_uuid4.return_value = uuid.UUID("12345678-1234-5678-1234-567812345678")
    mock_time.side_effect = [100.0, 100.5]  # Start time, end time
    
    # Create a mock request
    mock_request = MagicMock()
    mock_request.method = "GET"
    mock_request.url.path = "/api/v1/test"
    mock_request.client.host = "127.0.0.1"
    mock_request.state = MagicMock()
    
    # Create a mock call_next function that raises an exception
    mock_exception = Exception("Test exception")
    mock_call_next = AsyncMock(side_effect=mock_exception)
    
    # Create a mock app
    mock_app = MagicMock()
    
    # Initialize the middleware
    middleware = LoggingMiddleware(mock_app)
    
    # Call dispatch and expect an exception
    with pytest.raises(Exception) as excinfo:
        await middleware.dispatch(mock_request, mock_call_next)
    
    # Assert that the exception is the one we raised
    assert excinfo.value == mock_exception
    
    # Assert that the request ID was set on the request state
    assert mock_request.state.request_id == "12345678-1234-5678-1234-567812345678"
    
    # Assert that the request was logged
    mock_logger.info.assert_called_once_with(
        "Request 12345678-1234-5678-1234-567812345678: GET /api/v1/test from 127.0.0.1"
    )
    
    # Assert that call_next was called with the request
    mock_call_next.assert_called_once_with(mock_request)
    
    # Assert that the exception was logged
    mock_logger.error.assert_called_once_with(
        "Error 12345678-1234-5678-1234-567812345678: Test exception occurred after 0.5000s"
    )


def test_logger_configuration():
    """Test that the logger is configured correctly."""
    # Assert that the logger has the correct name
    assert logger.name == "vulcan-api"
    
    # Assert that the logger has the correct level
    assert logger.level == getattr(logging, "INFO")