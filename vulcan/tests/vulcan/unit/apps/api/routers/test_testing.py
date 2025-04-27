"""
Unit tests for the Vulcan API testing router.
"""
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi import HTTPException, status
from fastapi.testclient import TestClient

from vulcan.apps.api.routers.testing import router, run_tests
from vulcan.apps.api.models.requests import TestCodeRequest
from vulcan.apps.api.models.responses import TestCodeResponse, TestResult


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
@patch("vulcan.apps.api.routers.testing.TestingWorkflow")
async def test_run_tests_success(mock_workflow_class):
    """Test that run_tests returns a successful response when tests pass."""
    # Set up mocks
    mock_workflow = MagicMock()
    mock_workflow_class.return_value = mock_workflow
    
    mock_test_result1 = MagicMock()
    mock_test_result1.test_case.name = "test_factorial_positive"
    mock_test_result1.passed = True
    mock_test_result1.execution_time = 0.001
    mock_test_result1.error_message = None
    
    mock_test_result2 = MagicMock()
    mock_test_result2.test_case.name = "test_factorial_zero"
    mock_test_result2.passed = True
    mock_test_result2.execution_time = 0.001
    mock_test_result2.error_message = None
    
    mock_coverage = MagicMock()
    mock_coverage.line_coverage = 95.0
    mock_coverage.branch_coverage = 85.0
    mock_coverage.function_coverage = 100.0
    
    mock_result = MagicMock()
    mock_result.success = True
    mock_result.process_id = "abcd1234"
    mock_result.test_results = [mock_test_result1, mock_test_result2]
    mock_result.coverage = mock_coverage
    mock_result.error_message = None
    
    mock_workflow.execute_async = AsyncMock(return_value=mock_result)
    
    # Create a request
    request = TestCodeRequest(
        code_content={
            "factorial.py": "def factorial(n: int) -> int:\n    \"\"\"Calculate factorial.\"\"\"\n    if n == 0:\n        return 1\n    return n * factorial(n-1)"
        },
        generate_coverage=True,
    )
    
    # Call run_tests
    response = await run_tests(request, "test-api-key")
    
    # Assert that the workflow was executed with the correct arguments
    mock_workflow_class.assert_called_once()
    mock_workflow.execute_async.assert_called_once_with(
        code_content=request.code_content,
        generate_coverage=request.generate_coverage,
    )
    
    # Assert that the response is as expected
    assert response.success is True
    assert response.process_id == "abcd1234"
    assert len(response.test_results) == 2
    assert response.test_results[0]["name"] == "test_factorial_positive"
    assert response.test_results[0]["passed"] is True
    assert response.test_results[1]["name"] == "test_factorial_zero"
    assert response.test_results[1]["passed"] is True
    assert response.coverage["line"] == 95.0
    assert response.coverage["branch"] == 85.0
    assert response.coverage["function"] == 100.0
    assert response.error_message is None


@pytest.mark.asyncio
@patch("vulcan.apps.api.routers.testing.TestingWorkflow")
async def test_run_tests_failure(mock_workflow_class):
    """Test that run_tests returns a failure response when tests fail."""
    # Set up mocks
    mock_workflow = MagicMock()
    mock_workflow_class.return_value = mock_workflow
    
    mock_test_result1 = MagicMock()
    mock_test_result1.test_case.name = "test_factorial_positive"
    mock_test_result1.passed = True
    mock_test_result1.execution_time = 0.001
    mock_test_result1.error_message = None
    
    mock_test_result2 = MagicMock()
    mock_test_result2.test_case.name = "test_factorial_negative"
    mock_test_result2.passed = False
    mock_test_result2.execution_time = 0.001
    mock_test_result2.error_message = "AssertionError: Expected 120, got 60"
    
    mock_result = MagicMock()
    mock_result.success = True  # Workflow succeeded, but some tests failed
    mock_result.process_id = "abcd1234"
    mock_result.test_results = [mock_test_result1, mock_test_result2]
    mock_result.coverage = None
    mock_result.error_message = None
    
    mock_workflow.execute_async = AsyncMock(return_value=mock_result)
    
    # Create a request
    request = TestCodeRequest(
        code_content={
            "factorial.py": "def factorial(n: int) -> int:\n    \"\"\"Calculate factorial.\"\"\"\n    if n == 0:\n        return 1\n    return n * factorial(n-1)"
        },
        generate_coverage=False,
    )
    
    # Call run_tests
    response = await run_tests(request, "test-api-key")
    
    # Assert that the workflow was executed with the correct arguments
    mock_workflow_class.assert_called_once()
    mock_workflow.execute_async.assert_called_once_with(
        code_content=request.code_content,
        generate_coverage=request.generate_coverage,
    )
    
    # Assert that the response is as expected
    assert response.success is True
    assert response.process_id == "abcd1234"
    assert len(response.test_results) == 2
    assert response.test_results[0]["name"] == "test_factorial_positive"
    assert response.test_results[0]["passed"] is True
    assert response.test_results[1]["name"] == "test_factorial_negative"
    assert response.test_results[1]["passed"] is False
    assert response.test_results[1]["error_message"] == "AssertionError: Expected 120, got 60"
    assert response.coverage is None
    assert response.error_message is None


@pytest.mark.asyncio
@patch("vulcan.apps.api.routers.testing.TestingWorkflow")
async def test_run_tests_workflow_failure(mock_workflow_class):
    """Test that run_tests returns a failure response when the workflow fails."""
    # Set up mocks
    mock_workflow = MagicMock()
    mock_workflow_class.return_value = mock_workflow
    
    mock_result = MagicMock()
    mock_result.success = False
    mock_result.process_id = "abcd1234"
    mock_result.test_results = []
    mock_result.coverage = None
    mock_result.error_message = "Failed to run tests: Syntax error in code"
    
    mock_workflow.execute_async = AsyncMock(return_value=mock_result)
    
    # Create a request
    request = TestCodeRequest(
        code_content={
            "factorial.py": "def factorial(n: int) -> int:\n    \"\"\"Calculate factorial.\"\"\"\n    if n == 0:\n        return 1\n    return n * factorial(n-1"  # Missing closing parenthesis
        },
    )
    
    # Call run_tests
    response = await run_tests(request, "test-api-key")
    
    # Assert that the workflow was executed with the correct arguments
    mock_workflow_class.assert_called_once()
    mock_workflow.execute_async.assert_called_once()
    
    # Assert that the response is as expected
    assert response.success is False
    assert response.process_id == "abcd1234"
    assert len(response.test_results) == 0
    assert response.coverage is None
    assert response.error_message == "Failed to run tests: Syntax error in code"


@pytest.mark.asyncio
@patch("vulcan.apps.api.routers.testing.TestingWorkflow")
async def test_run_tests_exception(mock_workflow_class):
    """Test that run_tests raises an exception when an error occurs."""
    # Set up mocks
    mock_workflow = MagicMock()
    mock_workflow_class.return_value = mock_workflow
    
    mock_workflow.execute_async = AsyncMock(side_effect=Exception("Test exception"))
    
    # Create a request
    request = TestCodeRequest(
        code_content={
            "factorial.py": "def factorial(n: int) -> int:\n    \"\"\"Calculate factorial.\"\"\"\n    if n == 0:\n        return 1\n    return n * factorial(n-1)"
        },
    )
    
    # Call run_tests and expect an exception
    with pytest.raises(HTTPException) as excinfo:
        await run_tests(request, "test-api-key")
    
    # Assert that the exception has the expected status code and detail
    assert excinfo.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "Error running tests: Test exception" in excinfo.value.detail


def test_run_tests_endpoint(test_client):
    """Test that the run tests endpoint returns a successful response."""
    # Mock the run_tests function
    async def mock_run_tests(*args, **kwargs):
        return TestCodeResponse(
            success=True,
            process_id="abcd1234",
            test_results=[
                {
                    "name": "test_factorial_positive",
                    "passed": True,
                    "execution_time": 0.001,
                    "error_message": None,
                },
                {
                    "name": "test_factorial_zero",
                    "passed": True,
                    "execution_time": 0.001,
                    "error_message": None,
                },
            ],
            coverage={
                "line": 95.0,
                "branch": 85.0,
                "function": 100.0,
            },
        )
    
    with patch("vulcan.apps.api.routers.testing.run_tests", mock_run_tests):
        # Make a request to the endpoint
        response = test_client.post(
            "/api/v1/testing/run",
            json={
                "code_content": {
                    "factorial.py": "def factorial(n: int) -> int:\n    \"\"\"Calculate factorial.\"\"\"\n    if n == 0:\n        return 1\n    return n * factorial(n-1)"
                },
                "generate_coverage": True,
            },
            headers={"X-API-Key": "test-api-key"},
        )
        
        # Assert that the response is as expected
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["process_id"] == "abcd1234"
        assert len(data["test_results"]) == 2
        assert data["test_results"][0]["name"] == "test_factorial_positive"
        assert data["test_results"][0]["passed"] is True
        assert data["coverage"]["line"] == 95.0
        assert data["error_message"] is None


def test_run_tests_endpoint_error(test_client):
    """Test that the run tests endpoint returns an error response when an error occurs."""
    # Mock the run_tests function to raise an exception
    async def mock_run_tests(*args, **kwargs):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error running tests: Test exception",
        )
    
    with patch("vulcan.apps.api.routers.testing.run_tests", mock_run_tests):
        # Make a request to the endpoint
        response = test_client.post(
            "/api/v1/testing/run",
            json={
                "code_content": {
                    "factorial.py": "def factorial(n: int) -> int:\n    \"\"\"Calculate factorial.\"\"\"\n    if n == 0:\n        return 1\n    return n * factorial(n-1)"
                },
            },
            headers={"X-API-Key": "test-api-key"},
        )
        
        # Assert that the response is as expected
        assert response.status_code == 500
        data = response.json()
        assert data["detail"] == "Error running tests: Test exception"