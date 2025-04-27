"""
Unit tests for the Vulcan API code generation router.
"""
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi import HTTPException, status
from fastapi.testclient import TestClient

from vulcan.apps.api.routers.code_generation import router, generate_code
from vulcan.apps.api.models.requests import GenerateCodeRequest
from vulcan.apps.api.models.responses import GenerateCodeResponse, CodeArtifact


@pytest.fixture
def mock_verify_api_key():
    """Fixture to mock the API key verification."""
    with patch("vulcan.apps.api.middleware.auth.verify_api_key", return_value=True):
        yield


@pytest.fixture
def test_client(mock_verify_api_key):
    """Fixture to create a test client for the router."""
    from fastapi import FastAPI
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


@pytest.mark.asyncio
@patch("vulcan.apps.api.routers.code_generation.CodeGenerationWorkflow")
async def test_generate_code_success(mock_workflow_class):
    """Test that generate_code returns a successful response when code generation succeeds."""
    # Set up mocks
    mock_workflow = MagicMock()
    mock_workflow_class.return_value = mock_workflow
    
    mock_result = MagicMock()
    mock_result.success = True
    mock_result.process_id = "abcd1234"
    mock_result.artifacts = [
        MagicMock(
            file_path="factorial.py",
            content="def factorial(n: int) -> int:\n    \"\"\"Calculate factorial.\"\"\"\n    if n == 0:\n        return 1\n    return n * factorial(n-1)",
            language="python",
            metadata={"complexity": "O(n)"},
        )
    ]
    mock_result.error_message = None
    
    mock_workflow.execute_async = AsyncMock(return_value=mock_result)
    
    # Create a request
    request = GenerateCodeRequest(
        description="Create a Python function to calculate the factorial of a number",
        constraints=["Must include type hints", "Must include docstring"],
        examples=["factorial(5) -> 120", "factorial(0) -> 1"],
    )
    
    # Call generate_code
    response = await generate_code(request, "test-api-key")
    
    # Assert that the workflow was executed with the correct arguments
    mock_workflow_class.assert_called_once()
    mock_workflow.execute_async.assert_called_once()
    
    # Assert that the response is as expected
    assert response.success is True
    assert response.process_id == "abcd1234"
    assert len(response.artifacts) == 1
    assert response.artifacts[0]["file_path"] == "factorial.py"
    assert response.error_message is None


@pytest.mark.asyncio
@patch("vulcan.apps.api.routers.code_generation.CodeGenerationWorkflow")
async def test_generate_code_failure(mock_workflow_class):
    """Test that generate_code returns a failure response when code generation fails."""
    # Set up mocks
    mock_workflow = MagicMock()
    mock_workflow_class.return_value = mock_workflow
    
    mock_result = MagicMock()
    mock_result.success = False
    mock_result.process_id = "abcd1234"
    mock_result.artifacts = []
    mock_result.error_message = "Failed to generate code: Invalid requirements"
    
    mock_workflow.execute_async = AsyncMock(return_value=mock_result)
    
    # Create a request
    request = GenerateCodeRequest(
        description="Create a Python function to calculate the factorial of a number",
    )
    
    # Call generate_code
    response = await generate_code(request, "test-api-key")
    
    # Assert that the workflow was executed with the correct arguments
    mock_workflow_class.assert_called_once()
    mock_workflow.execute_async.assert_called_once()
    
    # Assert that the response is as expected
    assert response.success is False
    assert response.process_id == "abcd1234"
    assert len(response.artifacts) == 0
    assert response.error_message == "Failed to generate code: Invalid requirements"


@pytest.mark.asyncio
@patch("vulcan.apps.api.routers.code_generation.CodeGenerationWorkflow")
async def test_generate_code_exception(mock_workflow_class):
    """Test that generate_code raises an exception when an error occurs."""
    # Set up mocks
    mock_workflow = MagicMock()
    mock_workflow_class.return_value = mock_workflow
    
    mock_workflow.execute_async = AsyncMock(side_effect=Exception("Test exception"))
    
    # Create a request
    request = GenerateCodeRequest(
        description="Create a Python function to calculate the factorial of a number",
    )
    
    # Call generate_code and expect an exception
    with pytest.raises(HTTPException) as excinfo:
        await generate_code(request, "test-api-key")
    
    # Assert that the exception has the expected status code and detail
    assert excinfo.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "Error generating code: Test exception" in excinfo.value.detail


def test_generate_code_endpoint(test_client):
    """Test that the generate code endpoint returns a successful response."""
    # Mock the generate_code function
    async def mock_generate_code(*args, **kwargs):
        return GenerateCodeResponse(
            success=True,
            process_id="abcd1234",
            artifacts=[
                {
                    "file_path": "factorial.py",
                    "content": "def factorial(n: int) -> int:\n    \"\"\"Calculate factorial.\"\"\"\n    if n == 0:\n        return 1\n    return n * factorial(n-1)",
                    "language": "python",
                    "metadata": {"complexity": "O(n)"},
                }
            ],
        )
    
    with patch("vulcan.apps.api.routers.code_generation.generate_code", mock_generate_code):
        # Make a request to the endpoint
        response = test_client.post(
            "/api/v1/code-generation/generate",
            json={
                "description": "Create a Python function to calculate the factorial of a number",
                "constraints": ["Must include type hints", "Must include docstring"],
                "examples": ["factorial(5) -> 120", "factorial(0) -> 1"],
            },
            headers={"X-API-Key": "test-api-key"},
        )
        
        # Assert that the response is as expected
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["process_id"] == "abcd1234"
        assert len(data["artifacts"]) == 1
        assert data["artifacts"][0]["file_path"] == "factorial.py"
        assert data["error_message"] is None


def test_generate_code_endpoint_error(test_client):
    """Test that the generate code endpoint returns an error response when an error occurs."""
    # Mock the generate_code function to raise an exception
    async def mock_generate_code(*args, **kwargs):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error generating code: Test exception",
        )
    
    with patch("vulcan.apps.api.routers.code_generation.generate_code", mock_generate_code):
        # Make a request to the endpoint
        response = test_client.post(
            "/api/v1/code-generation/generate",
            json={
                "description": "Create a Python function to calculate the factorial of a number",
            },
            headers={"X-API-Key": "test-api-key"},
        )
        
        # Assert that the response is as expected
        assert response.status_code == 500
        data = response.json()
        assert data["detail"] == "Error generating code: Test exception"