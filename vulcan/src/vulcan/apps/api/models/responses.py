"""
Response models for the Vulcan API.
"""
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field


class CodeArtifact(BaseModel):
    """Model for a generated code artifact."""
    
    file_path: str = Field(
        ...,
        description="Path to the generated file",
        example="factorial.py",
    )
    
    content: str = Field(
        ...,
        description="Content of the generated file",
        example="def factorial(n: int) -> int:\n    \"\"\"Calculate factorial.\"\"\"\n    if n == 0:\n        return 1\n    return n * factorial(n-1)",
    )
    
    language: str = Field(
        ...,
        description="Programming language of the generated code",
        example="python",
    )
    
    metadata: Dict[str, str] = Field(
        default_factory=dict,
        description="Additional metadata for the generated code",
        example={"complexity": "O(n)", "author": "Vulcan"},
    )


class GenerateCodeResponse(BaseModel):
    """Response model for code generation."""
    
    success: bool = Field(
        ...,
        description="Whether the code generation was successful",
        example=True,
    )
    
    process_id: str = Field(
        ...,
        description="ID of the code generation process",
        example="abcd1234",
    )
    
    artifacts: List[CodeArtifact] = Field(
        default_factory=list,
        description="Generated code artifacts",
    )
    
    error_message: Optional[str] = Field(
        None,
        description="Error message if code generation failed",
        example="Failed to generate code: Invalid requirements",
    )


class TestResult(BaseModel):
    """Model for a test result."""
    
    name: str = Field(
        ...,
        description="Name of the test",
        example="test_factorial_positive",
    )
    
    passed: bool = Field(
        ...,
        description="Whether the test passed",
        example=True,
    )
    
    execution_time: float = Field(
        ...,
        description="Execution time of the test in seconds",
        example=0.001,
    )
    
    error_message: Optional[str] = Field(
        None,
        description="Error message if the test failed",
        example="AssertionError: Expected 120, got 60",
    )


class TestCodeResponse(BaseModel):
    """Response model for code testing."""
    
    success: bool = Field(
        ...,
        description="Whether the testing was successful",
        example=True,
    )
    
    process_id: str = Field(
        ...,
        description="ID of the testing process",
        example="abcd1234",
    )
    
    test_results: List[TestResult] = Field(
        default_factory=list,
        description="Results of the tests",
    )
    
    coverage: Optional[Dict[str, float]] = Field(
        None,
        description="Code coverage information",
        example={"line": 95.0, "branch": 85.0, "function": 100.0},
    )
    
    error_message: Optional[str] = Field(
        None,
        description="Error message if testing failed",
        example="Failed to run tests: Syntax error in code",
    )


class DeployCodeResponse(BaseModel):
    """Response model for code deployment."""
    
    success: bool = Field(
        ...,
        description="Whether the deployment was successful",
        example=True,
    )
    
    process_id: str = Field(
        ...,
        description="ID of the deployment process",
        example="abcd1234",
    )
    
    deployment_url: Optional[str] = Field(
        None,
        description="URL of the deployed code",
        example="https://github.com/username/repo/commit/abc123",
    )
    
    logs: List[str] = Field(
        default_factory=list,
        description="Deployment logs",
        example=["Cloning repository...", "Committing changes...", "Pushing to remote..."],
    )
    
    error_message: Optional[str] = Field(
        None,
        description="Error message if deployment failed",
        example="Failed to deploy code: Authentication failed",
    )


class ProcessStep(BaseModel):
    """Model for a process step."""
    
    name: str = Field(
        ...,
        description="Name of the step",
        example="Generate code",
    )
    
    status: str = Field(
        ...,
        description="Status of the step",
        example="completed",
    )
    
    start_time: str = Field(
        ...,
        description="Start time of the step",
        example="2023-06-01T12:00:00Z",
    )
    
    end_time: Optional[str] = Field(
        None,
        description="End time of the step",
        example="2023-06-01T12:01:00Z",
    )


class StatusResponse(BaseModel):
    """Response model for checking status."""
    
    process_id: str = Field(
        ...,
        description="ID of the process",
        example="abcd1234",
    )
    
    process_type: str = Field(
        ...,
        description="Type of the process",
        example="code_generation",
    )
    
    status: str = Field(
        ...,
        description="Status of the process",
        example="completed",
    )
    
    start_time: str = Field(
        ...,
        description="Start time of the process",
        example="2023-06-01T12:00:00Z",
    )
    
    end_time: Optional[str] = Field(
        None,
        description="End time of the process",
        example="2023-06-01T12:05:00Z",
    )
    
    steps: List[ProcessStep] = Field(
        default_factory=list,
        description="Steps of the process",
    )
    
    artifacts: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Artifacts produced by the process",
        example=[{"name": "factorial.py", "path": "/output/factorial.py"}],
    )
    
    errors: List[str] = Field(
        default_factory=list,
        description="Errors that occurred during the process",
        example=["Failed to generate test cases"],
    )


class ErrorResponse(BaseModel):
    """Response model for errors."""
    
    detail: str = Field(
        ...,
        description="Error message",
        example="Invalid API key",
    )