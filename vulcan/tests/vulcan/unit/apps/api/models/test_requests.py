"""
Unit tests for the Vulcan API request models.
"""
import pytest
from pydantic import ValidationError

from vulcan.apps.api.models.requests import (
    GenerateCodeRequest,
    TestCodeRequest,
    DeployCodeRequest,
    StatusRequest,
)


def test_generate_code_request_valid():
    """Test that a valid GenerateCodeRequest can be created."""
    # Create a valid request
    request = GenerateCodeRequest(
        description="Create a Python function to calculate the factorial of a number",
        constraints=["Must include type hints", "Must include docstring"],
        examples=["factorial(5) -> 120", "factorial(0) -> 1"],
    )
    
    # Assert that the request has the expected values
    assert request.description == "Create a Python function to calculate the factorial of a number"
    assert request.constraints == ["Must include type hints", "Must include docstring"]
    assert request.examples == ["factorial(5) -> 120", "factorial(0) -> 1"]


def test_generate_code_request_minimal():
    """Test that a minimal GenerateCodeRequest can be created."""
    # Create a minimal request
    request = GenerateCodeRequest(
        description="Create a Python function to calculate the factorial of a number",
    )
    
    # Assert that the request has the expected values
    assert request.description == "Create a Python function to calculate the factorial of a number"
    assert request.constraints is None
    assert request.examples is None


def test_generate_code_request_invalid():
    """Test that an invalid GenerateCodeRequest raises a validation error."""
    # Try to create an invalid request (missing required field)
    with pytest.raises(ValidationError):
        GenerateCodeRequest()


def test_test_code_request_valid():
    """Test that a valid TestCodeRequest can be created."""
    # Create a valid request
    request = TestCodeRequest(
        code_content={
            "factorial.py": "def factorial(n: int) -> int:\n    \"\"\"Calculate factorial.\"\"\"\n    if n == 0:\n        return 1\n    return n * factorial(n-1)"
        },
        generate_coverage=True,
    )
    
    # Assert that the request has the expected values
    assert "factorial.py" in request.code_content
    assert request.generate_coverage is True


def test_test_code_request_minimal():
    """Test that a minimal TestCodeRequest can be created."""
    # Create a minimal request
    request = TestCodeRequest(
        code_content={
            "factorial.py": "def factorial(n: int) -> int:\n    \"\"\"Calculate factorial.\"\"\"\n    if n == 0:\n        return 1\n    return n * factorial(n-1)"
        },
    )
    
    # Assert that the request has the expected values
    assert "factorial.py" in request.code_content
    assert request.generate_coverage is False


def test_test_code_request_invalid():
    """Test that an invalid TestCodeRequest raises a validation error."""
    # Try to create an invalid request (missing required field)
    with pytest.raises(ValidationError):
        TestCodeRequest()


def test_deploy_code_request_valid():
    """Test that a valid DeployCodeRequest can be created."""
    # Create a valid request
    request = DeployCodeRequest(
        code_content={
            "factorial.py": "def factorial(n: int) -> int:\n    \"\"\"Calculate factorial.\"\"\"\n    if n == 0:\n        return 1\n    return n * factorial(n-1)"
        },
        repository_url="https://github.com/username/repo.git",
        branch="main",
        commit_message="Add factorial function",
    )
    
    # Assert that the request has the expected values
    assert "factorial.py" in request.code_content
    assert request.repository_url == "https://github.com/username/repo.git"
    assert request.branch == "main"
    assert request.commit_message == "Add factorial function"


def test_deploy_code_request_minimal():
    """Test that a minimal DeployCodeRequest can be created."""
    # Create a minimal request
    request = DeployCodeRequest(
        code_content={
            "factorial.py": "def factorial(n: int) -> int:\n    \"\"\"Calculate factorial.\"\"\"\n    if n == 0:\n        return 1\n    return n * factorial(n-1)"
        },
        repository_url="https://github.com/username/repo.git",
    )
    
    # Assert that the request has the expected values
    assert "factorial.py" in request.code_content
    assert request.repository_url == "https://github.com/username/repo.git"
    assert request.branch == "main"  # Default value
    assert request.commit_message == "Deploy code via Vulcan API"  # Default value


def test_deploy_code_request_invalid():
    """Test that an invalid DeployCodeRequest raises a validation error."""
    # Try to create an invalid request (missing required fields)
    with pytest.raises(ValidationError):
        DeployCodeRequest()


def test_status_request_valid():
    """Test that a valid StatusRequest can be created."""
    # Create a valid request
    request = StatusRequest(
        process_id="abcd1234",
    )
    
    # Assert that the request has the expected values
    assert request.process_id == "abcd1234"


def test_status_request_invalid():
    """Test that an invalid StatusRequest raises a validation error."""
    # Try to create an invalid request (missing required field)
    with pytest.raises(ValidationError):
        StatusRequest()