"""
Unit tests for the Vulcan CLI config loader utilities.
"""
import sys
import pytest
from pathlib import Path
from unittest.mock import patch, mock_open, MagicMock

from vulcan.apps.cli.utils.config_loader import load_config_from_file, merge_configs


@patch("vulcan.apps.cli.utils.config_loader.importlib.util.spec_from_file_location")
@patch("vulcan.apps.cli.utils.config_loader.Path.exists")
def test_load_config_from_file_nonexistent(mock_exists, mock_spec_from_file_location):
    """Test that load_config_from_file handles non-existent files correctly."""
    # Set up mocks
    mock_exists.return_value = False
    
    # Call load_config_from_file
    config = load_config_from_file(Path("nonexistent.py"))
    
    # Assert that the result is an empty dictionary
    assert config == {}
    
    # Assert that spec_from_file_location was not called
    mock_spec_from_file_location.assert_not_called()


@patch("vulcan.apps.cli.utils.config_loader.importlib.util.spec_from_file_location")
@patch("vulcan.apps.cli.utils.config_loader.Path.exists")
def test_load_config_from_file_invalid_spec(mock_exists, mock_spec_from_file_location):
    """Test that load_config_from_file handles invalid files correctly."""
    # Set up mocks
    mock_exists.return_value = True
    mock_spec_from_file_location.return_value = None
    
    # Call load_config_from_file
    config = load_config_from_file(Path("invalid.py"))
    
    # Assert that the result is an empty dictionary
    assert config == {}
    
    # Assert that spec_from_file_location was called
    mock_spec_from_file_location.assert_called_once()


@patch("vulcan.apps.cli.utils.config_loader.importlib.util.spec_from_file_location")
@patch("vulcan.apps.cli.utils.config_loader.Path.exists")
def test_load_config_from_file_invalid_loader(mock_exists, mock_spec_from_file_location):
    """Test that load_config_from_file handles invalid loaders correctly."""
    # Set up mocks
    mock_exists.return_value = True
    mock_spec = MagicMock()
    mock_spec.loader = None
    mock_spec_from_file_location.return_value = mock_spec
    
    # Call load_config_from_file
    config = load_config_from_file(Path("invalid.py"))
    
    # Assert that the result is an empty dictionary
    assert config == {}
    
    # Assert that spec_from_file_location was called
    mock_spec_from_file_location.assert_called_once()


@patch("vulcan.apps.cli.utils.config_loader.importlib.util.module_from_spec")
@patch("vulcan.apps.cli.utils.config_loader.importlib.util.spec_from_file_location")
@patch("vulcan.apps.cli.utils.config_loader.Path.exists")
def test_load_config_from_file_valid(mock_exists, mock_spec_from_file_location, mock_module_from_spec):
    """Test that load_config_from_file loads configuration from a file correctly."""
    # Set up mocks
    mock_exists.return_value = True
    
    mock_spec = MagicMock()
    mock_spec_from_file_location.return_value = mock_spec
    
    mock_module = MagicMock()
    mock_module.__dict__ = {}
    mock_module.__dir__ = lambda: ["API_URL", "API_KEY", "__name__", "__file__"]
    mock_module.API_URL = "http://example.com"
    mock_module.API_KEY = "test-api-key"
    mock_module_from_spec.return_value = mock_module
    
    # Call load_config_from_file
    config = load_config_from_file(Path("config.py"))
    
    # Assert that the result contains the expected configuration
    assert config == {
        "API_URL": "http://example.com",
        "API_KEY": "test-api-key",
    }
    
    # Assert that spec_from_file_location was called
    mock_spec_from_file_location.assert_called_once()
    
    # Assert that module_from_spec was called
    mock_module_from_spec.assert_called_once()
    
    # Assert that exec_module was called
    mock_spec.loader.exec_module.assert_called_once_with(mock_module)


def test_merge_configs_simple():
    """Test that merge_configs merges two simple configuration dictionaries correctly."""
    # Set up test data
    base_config = {
        "API_URL": "http://example.com",
        "API_KEY": "test-api-key",
        "DEBUG": True,
    }
    
    override_config = {
        "API_URL": "http://override.com",
        "TIMEOUT": 30,
    }
    
    # Call merge_configs
    result = merge_configs(base_config, override_config)
    
    # Assert that the result contains the merged configuration
    assert result == {
        "API_URL": "http://override.com",  # Overridden
        "API_KEY": "test-api-key",         # From base
        "DEBUG": True,                     # From base
        "TIMEOUT": 30,                     # From override
    }


def test_merge_configs_nested():
    """Test that merge_configs merges nested configuration dictionaries correctly."""
    # Set up test data
    base_config = {
        "api": {
            "url": "http://example.com",
            "key": "test-api-key",
            "timeout": 10,
        },
        "debug": True,
    }
    
    override_config = {
        "api": {
            "url": "http://override.com",
            "version": "v1",
        },
        "logging": {
            "level": "INFO",
        },
    }
    
    # Call merge_configs
    result = merge_configs(base_config, override_config)
    
    # Assert that the result contains the merged configuration
    assert result == {
        "api": {
            "url": "http://override.com",  # Overridden
            "key": "test-api-key",         # From base
            "timeout": 10,                 # From base
            "version": "v1",               # From override
        },
        "debug": True,                     # From base
        "logging": {                       # From override
            "level": "INFO",
        },
    }


def test_merge_configs_override_non_dict():
    """Test that merge_configs handles overriding a non-dict value with a dict correctly."""
    # Set up test data
    base_config = {
        "api": "http://example.com",
    }
    
    override_config = {
        "api": {
            "url": "http://override.com",
        },
    }
    
    # Call merge_configs
    result = merge_configs(base_config, override_config)
    
    # Assert that the result contains the overridden configuration
    assert result == {
        "api": {
            "url": "http://override.com",
        },
    }


def test_merge_configs_override_dict_with_non_dict():
    """Test that merge_configs handles overriding a dict value with a non-dict correctly."""
    # Set up test data
    base_config = {
        "api": {
            "url": "http://example.com",
        },
    }
    
    override_config = {
        "api": "http://override.com",
    }
    
    # Call merge_configs
    result = merge_configs(base_config, override_config)
    
    # Assert that the result contains the overridden configuration
    assert result == {
        "api": "http://override.com",
    }