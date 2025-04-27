"""
Unit tests for the Vulcan API deployment router.
"""
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi import HTTPException, status
from fastapi.testclient import TestClient

from vulcan.apps.api.routers.deployment import router, deploy_code
from vulcan.apps.api.models.requests import DeployCodeRequest
from vulcan.apps.api.models.responses import DeployCodeResponse


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
@patch("vulcan.apps.api.routers.deployment.DeploymentWorkflow")
async def test_deploy_code_success(mock_workflow_class):
    """Test that deploy_code returns a successful response when deployment succeeds."""
    # Set up mocks
    mock_workflow = MagicMock()
    mock_workflow_class.return_value = mock_workflow
    
    mock_result = MagicMock()
    mock_result.success = True
    mock_result.process_id = "abcd1234"
    mock_result.deployment_url = "https://github.com/username/repo/commit/abc123"
    mock_result.logs = ["Cloning repository...", "Committing changes...", "Pushing to remote..."]
    mock_result.error_message = None
    
    mock_workflow.execute_async = AsyncMock(return_value=mock_result)
    
    # Create a request
    request = DeployCodeRequest(
        code_content={
            "factorial.py": "def factorial(n: int) -> int:\n    \"\"\"Calculate factorial.\"\"\"\n    if n == 0:\n        return 1\n    return n * factorial(n-1)"
        },
        repository_url="https://github.com/username/repo.git",
        branch="main",
        commit_message="Add factorial function",
    )
    
    # Call deploy_code
    response = await deploy_code(request, "test-api-key")
    
    # Assert that the workflow was executed with the correct arguments
    mock_workflow_class.assert_called_once()
    mock_workflow.execute_async.assert_called_once_with(
        code_content=request.code_content,
        repository_url=request.repository_url,
        branch=request.branch,
        commit_message=request.commit_message,
    )
    
    # Assert that the response is as expected
    assert response.success is True
    assert response.process_id == "abcd1234"
    assert response.deployment_url == "https://github.com/username/repo/commit/abc123"
    assert len(response.logs) == 3
    assert response.logs[0] == "Cloning repository..."
    assert response.error_message is None


@pytest.mark.asyncio
@patch("vulcan.apps.api.routers.deployment.DeploymentWorkflow")
async def test_deploy_code_failure(mock_workflow_class):
    """Test that deploy_code returns a failure response when deployment fails."""
    # Set up mocks
    mock_workflow = MagicMock()
    mock_workflow_class.return_value = mock_workflow
    
    mock_result = MagicMock()
    mock_result.success = False
    mock_result.process_id = "abcd1234"
    mock_result.deployment_url = None
    mock_result.logs = ["Cloning repository...", "Error: Authentication failed"]
    mock_result.error_message = "Failed to deploy code: Authentication failed"
    
    mock_workflow.execute_async = AsyncMock(return_value=mock_result)
    
    # Create a request
    request = DeployCodeRequest(
        code_content={
            "factorial.py": "def factorial(n: int) -> int:\n    \"\"\"Calculate factorial.\"\"\"\n    if n == 0:\n        return 1\n    return n * factorial(n-1)"
        },
        repository_url="https://github.com/username/repo.git",
        branch="main",
    )
    
    # Call deploy_code
    response = await deploy_code(request, "test-api-key")
    
    # Assert that the workflow was executed with the correct arguments
    mock_workflow_class.assert_called_once()
    mock_workflow.execute_async.assert_called_once()
    
    # Assert that the response is as expected
    assert response.success is False
    assert response.process_id == "abcd1234"
    assert response.deployment_url is None
    assert len(response.logs) == 2
    assert response.logs[1] == "Error: Authentication failed"
    assert response.error_message == "Failed to deploy code: Authentication failed"


@pytest.mark.asyncio
@patch("vulcan.apps.api.routers.deployment.DeploymentWorkflow")
async def test_deploy_code_exception(mock_workflow_class):
    """Test that deploy_code raises an exception when an error occurs."""
    # Set up mocks
    mock_workflow = MagicMock()
    mock_workflow_class.return_value = mock_workflow
    
    mock_workflow.execute_async = AsyncMock(side_effect=Exception("Test exception"))
    
    # Create a request
    request = DeployCodeRequest(
        code_content={
            "factorial.py": "def factorial(n: int) -> int:\n    \"\"\"Calculate factorial.\"\"\"\n    if n == 0:\n        return 1\n    return n * factorial(n-1)"
        },
        repository_url="https://github.com/username/repo.git",
    )
    
    # Call deploy_code and expect an exception
    with pytest.raises(HTTPException) as excinfo:
        await deploy_code(request, "test-api-key")
    
    # Assert that the exception has the expected status code and detail
    assert excinfo.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "Error deploying code: Test exception" in excinfo.value.detail


def test_deploy_code_endpoint(test_client):
    """Test that the deploy code endpoint returns a successful response."""
    # Mock the deploy_code function
    async def mock_deploy_code(*args, **kwargs):
        return DeployCodeResponse(
            success=True,
            process_id="abcd1234",
            deployment_url="https://github.com/username/repo/commit/abc123",
            logs=["Cloning repository...", "Committing changes...", "Pushing to remote..."],
        )
    
    with patch("vulcan.apps.api.routers.deployment.deploy_code", mock_deploy_code):
        # Make a request to the endpoint
        response = test_client.post(
            "/api/v1/deployment/deploy",
            json={
                "code_content": {
                    "factorial.py": "def factorial(n: int) -> int:\n    \"\"\"Calculate factorial.\"\"\"\n    if n == 0:\n        return 1\n    return n * factorial(n-1)"
                },
                "repository_url": "https://github.com/username/repo.git",
                "branch": "main",
                "commit_message": "Add factorial function",
            },
            headers={"X-API-Key": "test-api-key"},
        )
        
        # Assert that the response is as expected
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["process_id"] == "abcd1234"
        assert data["deployment_url"] == "https://github.com/username/repo/commit/abc123"
        assert len(data["logs"]) == 3
        assert data["logs"][0] == "Cloning repository..."
        assert data["error_message"] is None


def test_deploy_code_endpoint_error(test_client):
    """Test that the deploy code endpoint returns an error response when an error occurs."""
    # Mock the deploy_code function to raise an exception
    async def mock_deploy_code(*args, **kwargs):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deploying code: Test exception",
        )
    
    with patch("vulcan.apps.api.routers.deployment.deploy_code", mock_deploy_code):
        # Make a request to the endpoint
        response = test_client.post(
            "/api/v1/deployment/deploy",
            json={
                "code_content": {
                    "factorial.py": "def factorial(n: int) -> int:\n    \"\"\"Calculate factorial.\"\"\"\n    if n == 0:\n        return 1\n    return n * factorial(n-1)"
                },
                "repository_url": "https://github.com/username/repo.git",
            },
            headers={"X-API-Key": "test-api-key"},
        )
        
        # Assert that the response is as expected
        assert response.status_code == 500
        data = response.json()
        assert data["detail"] == "Error deploying code: Test exception"