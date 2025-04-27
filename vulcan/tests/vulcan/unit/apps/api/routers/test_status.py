"""
Unit tests for the Vulcan API status router.
"""
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi import HTTPException, status
from fastapi.testclient import TestClient

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../../../src')))

from vulcan.apps.api.routers.status import router, get_status, check_status
from vulcan.apps.api.models.requests import StatusRequest
from vulcan.apps.api.models.responses import StatusResponse, ProcessStep


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
@patch("vulcan.apps.api.routers.status.WorkflowStateManager")
async def test_get_status_success(mock_state_manager_class):
    """Test that get_status returns a successful response when the process is found."""
    # Set up mocks
    mock_state_manager = MagicMock()
    mock_state_manager_class.return_value = mock_state_manager

    mock_step1 = MagicMock()
    mock_step1.name = "Parse requirements"
    mock_step1.status.name = "COMPLETED"
    mock_step1.start_time = "2023-06-01T12:00:00Z"
    mock_step1.end_time = "2023-06-01T12:01:00Z"

    mock_step2 = MagicMock()
    mock_step2.name = "Generate code"
    mock_step2.status.name = "COMPLETED"
    mock_step2.start_time = "2023-06-01T12:01:00Z"
    mock_step2.end_time = "2023-06-01T12:05:00Z"

    mock_state = MagicMock()
    mock_state.process_id = "abcd1234"
    mock_state.process_type = "code_generation"
    mock_state.status.name = "COMPLETED"
    mock_state.start_time = "2023-06-01T12:00:00Z"
    mock_state.end_time = "2023-06-01T12:05:00Z"
    mock_state.steps = [mock_step1, mock_step2]
    mock_state.artifacts = [{"name": "factorial.py", "path": "/output/factorial.py"}]
    mock_state.errors = []

    mock_state_manager.get_state_async = AsyncMock(return_value=mock_state)

    # Call get_status
    response = await get_status("abcd1234", "test-api-key")

    # Assert that the state manager was called with the correct arguments
    mock_state_manager_class.assert_called_once()
    mock_state_manager.get_state_async.assert_called_once_with("abcd1234")

    # Assert that the response is as expected
    assert response.process_id == "abcd1234"
    assert response.process_type == "code_generation"
    assert response.status == "completed"
    assert response.start_time == "2023-06-01T12:00:00Z"
    assert response.end_time == "2023-06-01T12:05:00Z"
    assert len(response.steps) == 2
    assert response.steps[0]["name"] == "Parse requirements"
    assert response.steps[0]["status"] == "completed"
    assert response.steps[1]["name"] == "Generate code"
    assert response.steps[1]["status"] == "completed"
    assert len(response.artifacts) == 1
    assert response.artifacts[0]["name"] == "factorial.py"
    assert len(response.errors) == 0


@pytest.mark.asyncio
@patch("vulcan.apps.api.routers.status.WorkflowStateManager")
async def test_get_status_not_found(mock_state_manager_class):
    """Test that get_status raises an exception when the process is not found."""
    # Set up mocks
    mock_state_manager = MagicMock()
    mock_state_manager_class.return_value = mock_state_manager

    mock_state_manager.get_state_async = AsyncMock(return_value=None)

    # Call get_status and expect an exception
    with pytest.raises(HTTPException) as excinfo:
        await get_status("abcd1234", "test-api-key")

    # Assert that the state manager was called with the correct arguments
    mock_state_manager_class.assert_called_once()
    mock_state_manager.get_state_async.assert_called_once_with("abcd1234")

    # Assert that the exception has the expected status code and detail
    assert excinfo.value.status_code == status.HTTP_404_NOT_FOUND
    assert "Process not found: abcd1234" in excinfo.value.detail


@pytest.mark.asyncio
@patch("vulcan.apps.api.routers.status.WorkflowStateManager")
async def test_get_status_exception(mock_state_manager_class):
    """Test that get_status raises an exception when an error occurs."""
    # Set up mocks
    mock_state_manager = MagicMock()
    mock_state_manager_class.return_value = mock_state_manager

    mock_state_manager.get_state_async = AsyncMock(side_effect=Exception("Test exception"))

    # Call get_status and expect an exception
    with pytest.raises(HTTPException) as excinfo:
        await get_status("abcd1234", "test-api-key")

    # Assert that the state manager was called with the correct arguments
    mock_state_manager_class.assert_called_once()
    mock_state_manager.get_state_async.assert_called_once_with("abcd1234")

    # Assert that the exception has the expected status code and detail
    assert excinfo.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "Error checking status: Test exception" in excinfo.value.detail


@pytest.mark.asyncio
@patch("vulcan.apps.api.routers.status.get_status")
async def test_check_status(mock_get_status):
    """Test that check_status calls get_status with the correct arguments."""
    # Set up mocks
    mock_response = MagicMock()
    mock_get_status.return_value = mock_response

    # Create a request
    request = StatusRequest(
        process_id="abcd1234",
    )

    # Call check_status
    response = await check_status(request, "test-api-key")

    # Assert that get_status was called with the correct arguments
    mock_get_status.assert_called_once_with("abcd1234", "test-api-key")

    # Assert that the response is the one returned by get_status
    assert response == mock_response


def test_get_status_endpoint(test_client):
    """Test that the get status endpoint returns a successful response."""
    # Mock the get_status function
    async def mock_get_status(*args, **kwargs):
        return StatusResponse(
            process_id="abcd1234",
            process_type="code_generation",
            status="completed",
            start_time="2023-06-01T12:00:00Z",
            end_time="2023-06-01T12:05:00Z",
            steps=[
                {
                    "name": "Parse requirements",
                    "status": "completed",
                    "start_time": "2023-06-01T12:00:00Z",
                    "end_time": "2023-06-01T12:01:00Z",
                },
                {
                    "name": "Generate code",
                    "status": "completed",
                    "start_time": "2023-06-01T12:01:00Z",
                    "end_time": "2023-06-01T12:05:00Z",
                },
            ],
            artifacts=[
                {"name": "factorial.py", "path": "/output/factorial.py"}
            ],
        )

    with patch("vulcan.apps.api.routers.status.get_status", mock_get_status):
        # Make a request to the endpoint
        response = test_client.get(
            "/api/v1/status/abcd1234",
            headers={"X-API-Key": "test-api-key"},
        )

        # Assert that the response is as expected
        assert response.status_code == 200
        data = response.json()
        assert data["process_id"] == "abcd1234"
        assert data["process_type"] == "code_generation"
        assert data["status"] == "completed"
        assert data["start_time"] == "2023-06-01T12:00:00Z"
        assert data["end_time"] == "2023-06-01T12:05:00Z"
        assert len(data["steps"]) == 2
        assert data["steps"][0]["name"] == "Parse requirements"
        assert data["steps"][0]["status"] == "completed"
        assert data["steps"][1]["name"] == "Generate code"
        assert data["steps"][1]["status"] == "completed"
        assert len(data["artifacts"]) == 1
        assert data["artifacts"][0]["name"] == "factorial.py"
        assert len(data["errors"]) == 0


def test_get_status_endpoint_not_found(test_client):
    """Test that the get status endpoint returns a not found response when the process is not found."""
    # Mock the get_status function to raise an exception
    async def mock_get_status(*args, **kwargs):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Process not found: abcd1234",
        )

    with patch("vulcan.apps.api.routers.status.get_status", mock_get_status):
        # Make a request to the endpoint
        response = test_client.get(
            "/api/v1/status/abcd1234",
            headers={"X-API-Key": "test-api-key"},
        )

        # Assert that the response is as expected
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Process not found: abcd1234"


def test_check_status_endpoint(test_client):
    """Test that the check status endpoint returns a successful response."""
    # Mock the check_status function
    async def mock_check_status(*args, **kwargs):
        return StatusResponse(
            process_id="abcd1234",
            process_type="code_generation",
            status="completed",
            start_time="2023-06-01T12:00:00Z",
            end_time="2023-06-01T12:05:00Z",
            steps=[
                {
                    "name": "Parse requirements",
                    "status": "completed",
                    "start_time": "2023-06-01T12:00:00Z",
                    "end_time": "2023-06-01T12:01:00Z",
                },
                {
                    "name": "Generate code",
                    "status": "completed",
                    "start_time": "2023-06-01T12:01:00Z",
                    "end_time": "2023-06-01T12:05:00Z",
                },
            ],
            artifacts=[
                {"name": "factorial.py", "path": "/output/factorial.py"}
            ],
        )

    with patch("vulcan.apps.api.routers.status.check_status", mock_check_status):
        # Make a request to the endpoint
        response = test_client.post(
            "/api/v1/status/",
            json={"process_id": "abcd1234"},
            headers={"X-API-Key": "test-api-key"},
        )

        # Assert that the response is as expected
        assert response.status_code == 200
        data = response.json()
        assert data["process_id"] == "abcd1234"
        assert data["process_type"] == "code_generation"
        assert data["status"] == "completed"
        assert data["start_time"] == "2023-06-01T12:00:00Z"
        assert data["end_time"] == "2023-06-01T12:05:00Z"
        assert len(data["steps"]) == 2
        assert data["steps"][0]["name"] == "Parse requirements"
        assert data["steps"][0]["status"] == "completed"
        assert data["steps"][1]["name"] == "Generate code"
        assert data["steps"][1]["status"] == "completed"
        assert len(data["artifacts"]) == 1
        assert data["artifacts"][0]["name"] == "factorial.py"
        assert len(data["errors"]) == 0
