"""
Unit tests for the Vulcan API main module.
"""
import pytest
from unittest.mock import patch, MagicMock
from fastapi import FastAPI
from fastapi.testclient import TestClient

from vulcan.apps.api.main import app, root, health, start


def test_app_creation():
    """Test that the FastAPI application is created with the correct configuration."""
    # Assert that app is a FastAPI instance
    assert isinstance(app, FastAPI)
    
    # Assert that app has the correct configuration
    assert app.title == "Vulcan API"
    assert app.description == "API for the Vulcan autonomous coding agent"
    assert app.version == "0.1.0"
    assert app.docs_url == "/docs"
    assert app.redoc_url == "/redoc"


def test_middleware_addition():
    """Test that middleware is added correctly."""
    # Check that the app has middleware
    assert len(app.user_middleware) > 0
    
    # Check for CORS middleware
    cors_middleware = next(
        (m for m in app.user_middleware if m.cls.__name__ == "CORSMiddleware"),
        None,
    )
    assert cors_middleware is not None
    
    # Check for logging middleware
    logging_middleware = next(
        (m for m in app.user_middleware if m.cls.__name__ == "LoggingMiddleware"),
        None,
    )
    assert logging_middleware is not None


def test_router_inclusion():
    """Test that routers are included correctly."""
    # Check that the app has routes
    assert len(app.routes) > 0
    
    # Check for specific route prefixes
    route_prefixes = [route.path for route in app.routes]
    assert "/api/v1/code-generation" in "".join(route_prefixes)
    assert "/api/v1/testing" in "".join(route_prefixes)
    assert "/api/v1/deployment" in "".join(route_prefixes)
    assert "/api/v1/status" in "".join(route_prefixes)


def test_root_endpoint():
    """Test that the root endpoint returns the expected response."""
    # Create a test client
    client = TestClient(app)
    
    # Make a request to the root endpoint
    response = client.get("/")
    
    # Assert that the response is as expected
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "version": "0.1.0"}


def test_health_endpoint():
    """Test that the health endpoint returns the expected response."""
    # Create a test client
    client = TestClient(app)
    
    # Make a request to the health endpoint
    response = client.get("/health")
    
    # Assert that the response is as expected
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "version": "0.1.0"}

