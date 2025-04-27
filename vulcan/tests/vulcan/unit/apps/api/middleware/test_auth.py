"""
Unit tests for the Vulcan API auth middleware.
"""
from unittest.mock import patch, MagicMock
import pytest
from fastapi import HTTPException, status

from vulcan.apps.api.middleware.auth import (
    get_api_key,
    verify_api_key,
    api_key_header,
)


@pytest.mark.asyncio
async def test_get_api_key_valid():
    """Test that get_api_key returns the API key when it's provided."""
    # Call get_api_key with a valid API key
    api_key = await get_api_key("test-api-key")
    
    # Assert that the API key is returned
    assert api_key == "test-api-key"


@pytest.mark.asyncio
async def test_get_api_key_missing():
    """Test that get_api_key raises an exception when the API key is missing."""
    # Call get_api_key with a missing API key
    with pytest.raises(HTTPException) as excinfo:
        await get_api_key(None)
    
    # Assert that the exception has the expected status code and detail
    assert excinfo.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert excinfo.value.detail == "API key is missing"
    assert excinfo.value.headers["WWW-Authenticate"] == "X-API-Key"


@pytest.mark.asyncio
@patch("vulcan.apps.api.middleware.auth.API_KEY", "valid-api-key")
async def test_verify_api_key_valid():
    """Test that verify_api_key returns True when the API key is valid."""
    # Call verify_api_key with a valid API key
    result = await verify_api_key("valid-api-key")
    
    # Assert that the result is True
    assert result is True


@pytest.mark.asyncio
@patch("vulcan.apps.api.middleware.auth.API_KEY", "valid-api-key")
async def test_verify_api_key_invalid():
    """Test that verify_api_key raises an exception when the API key is invalid."""
    # Call verify_api_key with an invalid API key
    with pytest.raises(HTTPException) as excinfo:
        await verify_api_key("invalid-api-key")
    
    # Assert that the exception has the expected status code and detail
    assert excinfo.value.status_code == status.HTTP_403_FORBIDDEN
    assert excinfo.value.detail == "Invalid API key"
    assert excinfo.value.headers["WWW-Authenticate"] == "X-API-Key"


def test_api_key_header_configuration():
    """Test that the API key header is configured correctly."""
    # Assert that the API key header has the expected name
    assert api_key_header.name == "X-API-Key"
    
    # Assert that auto_error is False
    assert api_key_header.auto_error is False