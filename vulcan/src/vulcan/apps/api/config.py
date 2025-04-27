"""
Configuration for the Vulcan API.
"""
import os
from pathlib import Path

# API information
API_TITLE = "Vulcan API"
API_DESCRIPTION = "API for the Vulcan autonomous coding agent"
API_VERSION = "0.1.0"

# Paths
ROOT_DIR = Path(__file__).parent.parent.parent.parent.parent
CONFIG_DIR = ROOT_DIR / "config"

# Environment
ENV = os.environ.get("VULCAN_ENV", "development")

# CORS
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000",
    "https://vulcan-ui.example.com",
]

# Authentication
API_KEY_HEADER = "X-API-Key"
API_KEY = os.environ.get("VULCAN_API_KEY", "development-api-key")

# Rate limiting
RATE_LIMIT_ENABLED = os.environ.get("RATE_LIMIT_ENABLED", "true").lower() == "true"
RATE_LIMIT = int(os.environ.get("RATE_LIMIT", "100"))
RATE_LIMIT_PERIOD = int(os.environ.get("RATE_LIMIT_PERIOD", "3600"))  # in seconds

# Logging
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Timeouts
REQUEST_TIMEOUT = int(os.environ.get("REQUEST_TIMEOUT", "300"))  # in seconds

# Load environment-specific configuration
def load_env_config():
    """Load environment-specific configuration."""
    config_file = CONFIG_DIR / ENV / "app_config.py"
    if config_file.exists():
        # This is a simplified version; in a real app, you'd use importlib
        # to load the configuration module
        with open(config_file, "r") as f:
            exec(f.read(), globals())
    
    return {
        "API_TITLE": API_TITLE,
        "API_DESCRIPTION": API_DESCRIPTION,
        "API_VERSION": API_VERSION,
        "ALLOWED_ORIGINS": ALLOWED_ORIGINS,
        "API_KEY_HEADER": API_KEY_HEADER,
        "API_KEY": API_KEY,
        "RATE_LIMIT_ENABLED": RATE_LIMIT_ENABLED,
        "RATE_LIMIT": RATE_LIMIT,
        "RATE_LIMIT_PERIOD": RATE_LIMIT_PERIOD,
        "LOG_LEVEL": LOG_LEVEL,
        "LOG_FORMAT": LOG_FORMAT,
        "REQUEST_TIMEOUT": REQUEST_TIMEOUT,
    }