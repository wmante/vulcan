"""
Unit tests for the Vulcan API response models.
"""
import pytest
from pydantic import ValidationError

from vulcan.apps.api.models.responses import (
    CodeArtifact,
    GenerateCodeResponse,
    TestResult,
    TestCodeResponse,
    DeployCodeResponse,
    ProcessStep,
    StatusResponse,
    ErrorResponse,
)


def test_code_artifact_valid():
    """Test that a valid CodeArtifact can be created."""
    # Create a valid artifact
    artifact = CodeArtifact(
        file_path="factorial.py",
        content="def factorial(n: int) -> int:\n    \"\"\"Calculate factorial.\"\"\"\n    if n == 0:\n        return 1\n    return n * factorial(n-1)",
        language="python",
        metadata={"complexity": "O(n)", "author": "Vulcan"},
    )
    
    # Assert that the artifact has the expected values
    assert artifact.file_path == "factorial.py"
    assert "def factorial" in artifact.content
    assert artifact.language == "python"
    assert artifact.metadata["complexity"] == "O(n)"
    assert artifact.metadata["author"] == "Vulcan"


def test_code_artifact_minimal():
    """Test that a minimal CodeArtifact can be created."""
    # Create a minimal artifact
    artifact = CodeArtifact(
        file_path="factorial.py",
        content="def factorial(n: int) -> int:\n    \"\"\"Calculate factorial.\"\"\"\n    if n == 0:\n        return 1\n    return n * factorial(n-1)",
        language="python",
    )
    
    # Assert that the artifact has the expected values
    assert artifact.file_path == "factorial.py"
    assert "def factorial" in artifact.content
    assert artifact.language == "python"
    assert artifact.metadata == {}


def test_code_artifact_invalid():
    """Test that an invalid CodeArtifact raises a validation error."""
    # Try to create an invalid artifact (missing required fields)
    with pytest.raises(ValidationError):
        CodeArtifact()


def test_generate_code_response_success():
    """Test that a successful GenerateCodeResponse can be created."""
    # Create a successful response
    response = GenerateCodeResponse(
        success=True,
        process_id="abcd1234",
        artifacts=[
            CodeArtifact(
                file_path="factorial.py",
                content="def factorial(n: int) -> int:\n    \"\"\"Calculate factorial.\"\"\"\n    if n == 0:\n        return 1\n    return n * factorial(n-1)",
                language="python",
            ),
        ],
    )
    
    # Assert that the response has the expected values
    assert response.success is True
    assert response.process_id == "abcd1234"
    assert len(response.artifacts) == 1
    assert response.artifacts[0].file_path == "factorial.py"
    assert response.error_message is None


def test_generate_code_response_failure():
    """Test that a failure GenerateCodeResponse can be created."""
    # Create a failure response
    response = GenerateCodeResponse(
        success=False,
        process_id="abcd1234",
        error_message="Failed to generate code: Invalid requirements",
    )
    
    # Assert that the response has the expected values
    assert response.success is False
    assert response.process_id == "abcd1234"
    assert len(response.artifacts) == 0
    assert response.error_message == "Failed to generate code: Invalid requirements"


def test_test_result_valid():
    """Test that a valid TestResult can be created."""
    # Create a valid test result
    result = TestResult(
        name="test_factorial_positive",
        passed=True,
        execution_time=0.001,
    )
    
    # Assert that the result has the expected values
    assert result.name == "test_factorial_positive"
    assert result.passed is True
    assert result.execution_time == 0.001
    assert result.error_message is None


def test_test_result_failure():
    """Test that a failure TestResult can be created."""
    # Create a failure test result
    result = TestResult(
        name="test_factorial_negative",
        passed=False,
        execution_time=0.001,
        error_message="AssertionError: Expected 120, got 60",
    )
    
    # Assert that the result has the expected values
    assert result.name == "test_factorial_negative"
    assert result.passed is False
    assert result.execution_time == 0.001
    assert result.error_message == "AssertionError: Expected 120, got 60"


def test_test_code_response_success():
    """Test that a successful TestCodeResponse can be created."""
    # Create a successful response
    response = TestCodeResponse(
        success=True,
        process_id="abcd1234",
        test_results=[
            TestResult(
                name="test_factorial_positive",
                passed=True,
                execution_time=0.001,
            ),
            TestResult(
                name="test_factorial_zero",
                passed=True,
                execution_time=0.001,
            ),
        ],
        coverage={"line": 95.0, "branch": 85.0, "function": 100.0},
    )
    
    # Assert that the response has the expected values
    assert response.success is True
    assert response.process_id == "abcd1234"
    assert len(response.test_results) == 2
    assert response.test_results[0].name == "test_factorial_positive"
    assert response.test_results[1].name == "test_factorial_zero"
    assert response.coverage["line"] == 95.0
    assert response.coverage["branch"] == 85.0
    assert response.coverage["function"] == 100.0
    assert response.error_message is None


def test_test_code_response_failure():
    """Test that a failure TestCodeResponse can be created."""
    # Create a failure response
    response = TestCodeResponse(
        success=False,
        process_id="abcd1234",
        error_message="Failed to run tests: Syntax error in code",
    )
    
    # Assert that the response has the expected values
    assert response.success is False
    assert response.process_id == "abcd1234"
    assert len(response.test_results) == 0
    assert response.coverage is None
    assert response.error_message == "Failed to run tests: Syntax error in code"


def test_deploy_code_response_success():
    """Test that a successful DeployCodeResponse can be created."""
    # Create a successful response
    response = DeployCodeResponse(
        success=True,
        process_id="abcd1234",
        deployment_url="https://github.com/username/repo/commit/abc123",
        logs=["Cloning repository...", "Committing changes...", "Pushing to remote..."],
    )
    
    # Assert that the response has the expected values
    assert response.success is True
    assert response.process_id == "abcd1234"
    assert response.deployment_url == "https://github.com/username/repo/commit/abc123"
    assert len(response.logs) == 3
    assert response.logs[0] == "Cloning repository..."
    assert response.error_message is None


def test_deploy_code_response_failure():
    """Test that a failure DeployCodeResponse can be created."""
    # Create a failure response
    response = DeployCodeResponse(
        success=False,
        process_id="abcd1234",
        logs=["Cloning repository...", "Error: Authentication failed"],
        error_message="Failed to deploy code: Authentication failed",
    )
    
    # Assert that the response has the expected values
    assert response.success is False
    assert response.process_id == "abcd1234"
    assert response.deployment_url is None
    assert len(response.logs) == 2
    assert response.logs[1] == "Error: Authentication failed"
    assert response.error_message == "Failed to deploy code: Authentication failed"


def test_process_step_valid():
    """Test that a valid ProcessStep can be created."""
    # Create a valid process step
    step = ProcessStep(
        name="Generate code",
        status="completed",
        start_time="2023-06-01T12:00:00Z",
        end_time="2023-06-01T12:01:00Z",
    )
    
    # Assert that the step has the expected values
    assert step.name == "Generate code"
    assert step.status == "completed"
    assert step.start_time == "2023-06-01T12:00:00Z"
    assert step.end_time == "2023-06-01T12:01:00Z"


def test_process_step_in_progress():
    """Test that an in-progress ProcessStep can be created."""
    # Create an in-progress process step
    step = ProcessStep(
        name="Generate code",
        status="in_progress",
        start_time="2023-06-01T12:00:00Z",
    )
    
    # Assert that the step has the expected values
    assert step.name == "Generate code"
    assert step.status == "in_progress"
    assert step.start_time == "2023-06-01T12:00:00Z"
    assert step.end_time is None


def test_status_response_valid():
    """Test that a valid StatusResponse can be created."""
    # Create a valid status response
    response = StatusResponse(
        process_id="abcd1234",
        process_type="code_generation",
        status="completed",
        start_time="2023-06-01T12:00:00Z",
        end_time="2023-06-01T12:05:00Z",
        steps=[
            ProcessStep(
                name="Parse requirements",
                status="completed",
                start_time="2023-06-01T12:00:00Z",
                end_time="2023-06-01T12:01:00Z",
            ),
            ProcessStep(
                name="Generate code",
                status="completed",
                start_time="2023-06-01T12:01:00Z",
                end_time="2023-06-01T12:05:00Z",
            ),
        ],
        artifacts=[
            {"name": "factorial.py", "path": "/output/factorial.py"}
        ],
    )
    
    # Assert that the response has the expected values
    assert response.process_id == "abcd1234"
    assert response.process_type == "code_generation"
    assert response.status == "completed"
    assert response.start_time == "2023-06-01T12:00:00Z"
    assert response.end_time == "2023-06-01T12:05:00Z"
    assert len(response.steps) == 2
    assert response.steps[0].name == "Parse requirements"
    assert response.steps[1].name == "Generate code"
    assert len(response.artifacts) == 1
    assert response.artifacts[0]["name"] == "factorial.py"
    assert len(response.errors) == 0


def test_status_response_with_errors():
    """Test that a StatusResponse with errors can be created."""
    # Create a status response with errors
    response = StatusResponse(
        process_id="abcd1234",
        process_type="code_generation",
        status="failed",
        start_time="2023-06-01T12:00:00Z",
        end_time="2023-06-01T12:05:00Z",
        errors=["Failed to parse requirements", "Invalid syntax in generated code"],
    )
    
    # Assert that the response has the expected values
    assert response.process_id == "abcd1234"
    assert response.process_type == "code_generation"
    assert response.status == "failed"
    assert len(response.errors) == 2
    assert response.errors[0] == "Failed to parse requirements"
    assert response.errors[1] == "Invalid syntax in generated code"


def test_error_response_valid():
    """Test that a valid ErrorResponse can be created."""
    # Create a valid error response
    response = ErrorResponse(
        detail="Invalid API key",
    )
    
    # Assert that the response has the expected values
    assert response.detail == "Invalid API key"