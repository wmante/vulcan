"""
Unit tests for the Vulcan API config module.
"""
import os
from pathlib import Path
from unittest.mock import patch, mock_open

from vulcan.apps.api.config import (
    API_TITLE,
    API_DESCRIPTION,
    API_VERSION,
    ROOT_DIR,
    CONFIG_DIR,
    ENV,
    ALLOWED_ORIGINS,
    API_KEY_HEADER,
    API_KEY,
    RATE_LIMIT_ENABLED,
    RATE_LIMIT,
    RATE_LIMIT_PERIOD,
    LOG_LEVEL,
    LOG_FORMAT,
    REQUEST_TIMEOUT,
    load_env_config,
)


def test_constants():
    """Test that the constants are defined correctly."""
    # Test API information
    assert API_TITLE == "Vulcan API"
    assert API_DESCRIPTION == "API for the Vulcan autonomous coding agent"
    assert API_VERSION == "0.1.0"
    
    # Test paths
    assert ROOT_DIR.is_absolute()
    assert CONFIG_DIR == ROOT_DIR / "config"
    
    # Test environment
    assert ENV in ["development", "testing", "production"]
    
    # Test CORS
    assert isinstance(ALLOWED_ORIGINS, list)
    assert "http://localhost:3000" in ALLOWED_ORIGINS
    assert "http://localhost:8000" in ALLOWED_ORIGINS
    
    # Test authentication
    assert API_KEY_HEADER == "X-API-Key"
    assert API_KEY is not None
    
    # Test rate limiting
    assert isinstance(RATE_LIMIT_ENABLED, bool)
    assert isinstance(RATE_LIMIT, int)
    assert isinstance(RATE_LIMIT_PERIOD, int)
    
    # Test logging
    assert LOG_LEVEL in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    assert LOG_FORMAT is not None
    
    # Test timeouts
    assert isinstance(REQUEST_TIMEOUT, int)


@patch("vulcan.apps.api.config.CONFIG_DIR")
@patch("vulcan.apps.api.config.ENV", "development")
@patch("builtins.open", new_callable=mock_open, read_data="API_TITLE = 'Custom API Title'")
def test_load_env_config_file_exists(mock_file, mock_config_dir):
    """Test that load_env_config loads configuration from a file when it exists."""
    # Set up mocks
    mock_path = Path("/mock/config/development/app_config.py")
    mock_config_dir = Path("/mock/config")
    mock_path.exists = lambda: True
    
    with patch("vulcan.apps.api.config.CONFIG_DIR / ENV / 'app_config.py'", mock_path):
        # Call load_env_config
        config = load_env_config()
        
        # Assert that the file was opened
        mock_file.assert_called_once_with(mock_path, "r")
        
        # Assert that the config contains the expected values
        assert config["API_TITLE"] == "Vulcan API"
        assert config["API_DESCRIPTION"] == "API for the Vulcan autonomous coding agent"
        assert config["API_VERSION"] == "0.1.0"


@patch("vulcan.apps.api.config.CONFIG_DIR")
@patch("vulcan.apps.api.config.ENV", "development")
def test_load_env_config_file_not_exists(mock_config_dir):
    """Test that load_env_config returns default configuration when the file doesn't exist."""
    # Set up mocks
    mock_path = Path("/mock/config/development/app_config.py")
    mock_config_dir = Path("/mock/config")
    mock_path.exists = lambda: False
    
    with patch("vulcan.apps.api.config.CONFIG_DIR / ENV / 'app_config.py'", mock_path):
        # Call load_env_config
        config = load_env_config()
        
        # Assert that the config contains the expected values
        assert config["API_TITLE"] == "Vulcan API"
        assert config["API_DESCRIPTION"] == "API for the Vulcan autonomous coding agent"
        assert config["API_VERSION"] == "0.1.0"


@patch.dict(os.environ, {"VULCAN_ENV": "production"})
def test_env_from_environment_variable():
    """Test that ENV is set from the environment variable."""
    # Import the module again to reload the constants
    from importlib import reload
    from vulcan.apps.api import config
    reload(config)
    
    # Assert that ENV is set from the environment variable
    assert config.ENV == "production"


@patch.dict(os.environ, {"VULCAN_API_KEY": "test-api-key"})
def test_api_key_from_environment_variable():
    """Test that API_KEY is set from the environment variable."""
    # Import the module again to reload the constants
    from importlib import reload
    from vulcan.apps.api import config
    reload(config)
    
    # Assert that API_KEY is set from the environment variable
    assert config.API_KEY == "test-api-key"