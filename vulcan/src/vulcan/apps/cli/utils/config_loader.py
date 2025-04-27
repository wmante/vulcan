"""
Configuration loader for the Vulcan CLI.
"""
import importlib.util
import sys
from pathlib import Path
from typing import Dict, Any


def load_config_from_file(file_path: Path) -> Dict[str, Any]:
    """
    Load configuration from a Python file.
    
    Args:
        file_path: Path to the configuration file
        
    Returns:
        Dictionary containing the configuration
    """
    if not file_path.exists():
        return {}
    
    # Load the module
    module_name = file_path.stem
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        return {}
    
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    
    # Extract configuration
    config = {}
    for key in dir(module):
        if not key.startswith("__"):
            config[key] = getattr(module, key)
    
    return config


def merge_configs(base_config: Dict[str, Any], override_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge two configuration dictionaries.
    
    Args:
        base_config: Base configuration
        override_config: Configuration to override base
        
    Returns:
        Merged configuration
    """
    result = base_config.copy()
    
    for key, value in override_config.items():
        if (
            key in result
            and isinstance(result[key], dict)
            and isinstance(value, dict)
        ):
            result[key] = merge_configs(result[key], value)
        else:
            result[key] = value
    
    return result