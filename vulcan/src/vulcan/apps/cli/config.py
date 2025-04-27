"""
Configuration for the Vulcan CLI.
"""
import os
from pathlib import Path
from typing import Dict, Any

# CLI version
CLI_VERSION = "0.1.0"

# Paths
ROOT_DIR = Path(__file__).parent.parent.parent.parent.parent
CONFIG_DIR = ROOT_DIR / "config"
DEFAULT_OUTPUT_DIR = ROOT_DIR / "output"

# Environment
ENV = os.environ.get("VULCAN_ENV", "development")

# Configuration files
CONFIG_FILES = {
    "default": CONFIG_DIR / "default" / "app_config.py",
    "development": CONFIG_DIR / "development" / "app_config.py",
    "testing": CONFIG_DIR / "testing" / "app_config.py",
    "production": CONFIG_DIR / "production" / "app_config.py",
}

# Default configuration
DEFAULT_CONFIG: Dict[str, Any] = {
    "llm": {
        "provider": "dust",
        "model": "gpt-4",
        "temperature": 0.7,
        "max_tokens": 2000,
    },
    "github": {
        "api_url": "https://api.github.com",
        "default_branch": "main",
    },
    "testing": {
        "framework": "pytest",
        "coverage_threshold": 80,
    },
}

# Load configuration from file
def load_config() -> Dict[str, Any]:
    """Load configuration from file based on environment."""
    from vulcan.apps.cli.utils.config_loader import load_config_from_file
    
    config = DEFAULT_CONFIG.copy()
    
    # Load default config
    if CONFIG_FILES["default"].exists():
        default_config = load_config_from_file(CONFIG_FILES["default"])
        config.update(default_config)
    
    # Load environment-specific config
    if ENV in CONFIG_FILES and CONFIG_FILES[ENV].exists():
        env_config = load_config_from_file(CONFIG_FILES[ENV])
        config.update(env_config)
    
    return config