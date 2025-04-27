"""
Request models for the Vulcan API.
"""
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class GenerateCodeRequest(BaseModel):
    """Request model for code generation."""
    
    description: str = Field(
        ...,
        description="Description of the code to generate",
        example="Create a Python function to calculate the factorial of a number",
    )
    
    constraints: Optional[List[str]] = Field(
        None,
        description="Constraints for the generated code",
        example=["Must include type hints", "Must include docstring"],
    )
    
    examples: Optional[List[str]] = Field(
        None,
        description="Examples of expected behavior",
        example=["factorial(5) -> 120", "factorial(0) -> 1"],
    )


class TestCodeRequest(BaseModel):
    """Request model for code testing."""
    
    code_content: Dict[str, str] = Field(
        ...,
        description="Dictionary mapping file paths to code content",
        example={
            "factorial.py": "def factorial(n: int) -> int:\n    \"\"\"Calculate factorial.\"\"\"\n    if n == 0:\n        return 1\n    return n * factorial(n-1)"
        },
    )
    
    generate_coverage: bool = Field(
        False,
        description="Whether to generate coverage report",
    )


class DeployCodeRequest(BaseModel):
    """Request model for code deployment."""
    
    code_content: Dict[str, str] = Field(
        ...,
        description="Dictionary mapping file paths to code content",
        example={
            "factorial.py": "def factorial(n: int) -> int:\n    \"\"\"Calculate factorial.\"\"\"\n    if n == 0:\n        return 1\n    return n * factorial(n-1)"
        },
    )
    
    repository_url: str = Field(
        ...,
        description="GitHub repository URL",
        example="https://github.com/username/repo.git",
    )
    
    branch: str = Field(
        "main",
        description="Branch to deploy to",
        example="main",
    )
    
    commit_message: str = Field(
        "Deploy code via Vulcan API",
        description="Commit message",
        example="Add factorial function",
    )


class StatusRequest(BaseModel):
    """Request model for checking status."""
    
    process_id: str = Field(
        ...,
        description="ID of the process to check",
        example="abcd1234",
    )