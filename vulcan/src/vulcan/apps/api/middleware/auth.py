"""
Authentication middleware for the Vulcan API.
"""
from fastapi import Header, HTTPException, Depends, status
from fastapi.security import APIKeyHeader
from typing import Optional

from vulcan.apps.api.config import API_KEY, API_KEY_HEADER


# API key security scheme
api_key_header = APIKeyHeader(name=API_KEY_HEADER, auto_error=False)


async def get_api_key(
    api_key: Optional[str] = Depends(api_key_header),
) -> str:
    """
    Get and validate the API key from the request header.
    
    Args:
        api_key: API key from the request header
        
    Returns:
        Validated API key
        
    Raises:
        HTTPException: If the API key is missing or invalid
    """
    if api_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key is missing",
            headers={"WWW-Authenticate": API_KEY_HEADER},
        )
    
    return api_key


async def verify_api_key(api_key: str = Depends(get_api_key)) -> bool:
    """
    Verify that the API key is valid.
    
    Args:
        api_key: API key to verify
        
    Returns:
        True if the API key is valid
        
    Raises:
        HTTPException: If the API key is invalid
    """
    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key",
            headers={"WWW-Authenticate": API_KEY_HEADER},
        )
    
    return True