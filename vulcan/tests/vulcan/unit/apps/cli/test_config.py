"""
Unit tests for the Vulcan CLI config module.
"""
import os
import pytest
from pathlib import Path
from unittest.mock import patch, mock_open, MagicMock

from vulcan.apps.cli.config import (
    CLI_VERSION,
    ROOT_DIR,
    CONFIG_DIR,
    DEFAULT_OUTPUT_DIR,
    ENV,
    CONFIG_FILES,
    DEFAULT_CONFIG,
    load_config,
)


def test_constants():
    """Test that the constants are defined correctly."""
    # Test CLI version
    assert CLI_VERSION == "0.1.0"
    
    # Test paths
    assert ROOT_DIR.is_absolute()
    assert CONFIG_DIR == ROOT_DIR / "config"
    assert DEFAULT_OUTPUT_DIR == ROOT_DIR / "output"
    
    # Test environment
    assert ENV in ["development", "testing", "production"]
    
    # Test configuration files
    assert "default" in CONFIG_FILES
    assert "development" in CONFIG_FILES
    assert "testing" in CONFIG_FILES
    assert "production" in CONFIG_FILES
    
    # Test default configuration
    assert "llm" in DEFAULT_CONFIG
    assert "github" in DEFAULT_CONFIG
    assert "testing" in DEFAULT_CONFIG


@patch("vulcan.apps.cli.config.load_config_from_file")
@patch("vulcan.apps.cli.config.CONFIG_FILES")
@patch("vulcan.apps.cli.config.ENV", "development")
def test_load_config_default_only(mock_config_files, mock_load_config_from_file):
    """Test that load_config loads only the default configuration when environment config doesn't exist."""
    # Set up mocks
    mock_config_files.__getitem__.return_value = MagicMock()
    mock_config_files.__getitem__.return_value.exists.return_value = True
    mock_load_config_from_file.return_value = {"llm": {"model": "gpt-3.5-turbo"}}
    
    # Call load_config
    config = load_config()
    
    # Assert that load_config_from_file was called with the default config file
    mock_load_config_from_file.assert_called_once()
    
    # Assert that the config contains the default configuration
    assert config["llm"]["provider"] == "dust"
    assert config["llm"]["model"] == "gpt-3.5-turbo"  # Overridden by default config
    assert config["github"]["api_url"] == "https://api.github.com"
    assert config["testing"]["framework"] == "pytest"


@patch("vulcan.apps.cli.config.load_config_from_file")
@patch("vulcan.apps.cli.config.CONFIG_FILES")
@patch("vulcan.apps.cli.config.ENV", "development")
def test_load_config_with_env(mock_config_files, mock_load_config_from_file):
    """Test that load_config loads and merges both default and environment configurations."""
    # Set up mocks for default config
    default_config_file = MagicMock()
    default_config_file.exists.return_value = True
    
    # Set up mocks for environment config
    env_config_file = MagicMock()
    env_config_file.exists.return_value = True
    
    # Set up mock for CONFIG_FILES
    mock_config_files.__getitem__.side_effect = lambda key: default_config_file if key == "default" else env_config_file
    mock_config_files.__contains__.return_value = True
    
    # Set up mock for load_config_from_file
    mock_load_config_from_file.side_effect = [
        {"llm": {"model": "gpt-3.5-turbo"}},  # Default config
        {"llm": {"temperature": 0.5}, "github": {"default_branch": "develop"}},  # Environment config
    ]
    
    # Call load_config
    config = load_config()
    
    # Assert that load_config_from_file was called twice
    assert mock_load_config_from_file.call_count == 2
    
    # Assert that the config contains the merged configuration
    assert config["llm"]["provider"] == "dust"
    assert config["llm"]["model"] == "gpt-3.5-turbo"  # Overridden by default config
    assert config["llm"]["temperature"] == 0.5  # Overridden by environment config
    assert config["github"]["api_url"] == "https://api.github.com"
    assert config["github"]["default_branch"] == "develop"  # Overridden by environment config
    assert config["testing"]["framework"] == "pytest"


@patch("vulcan.apps.cli.config.load_config_from_file")
@patch("vulcan.apps.cli.config.CONFIG_FILES")
@patch("vulcan.apps.cli.config.ENV", "development")
def test_load_config_no_files(mock_config_files, mock_load_config_from_file):
    """Test that load_config returns the default configuration when no config files exist."""
    # Set up mocks
    mock_config_files.__getitem__.return_value = MagicMock()
    mock_config_files.__getitem__.return_value.exists.return_value = False
    
    # Call load_config
    config = load_config()
    
    # Assert that load_config_from_file was not called
    mock_load_config_from_file.assert_not_called()
    
    # Assert that the config contains the default configuration
    assert config["llm"]["provider"] == "dust"
    assert config["llm"]["model"] == "gpt-4"
    assert config["github"]["api_url"] == "https://api.github.com"
    assert config["testing"]["framework"] == "pytest"