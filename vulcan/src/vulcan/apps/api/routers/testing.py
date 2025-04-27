"""
Router for testing endpoints.
"""
import logging
from fastapi import APIRouter, Depends, HTTPException, status

from vulcan.apps.api.middleware.auth import get_api_key
from vulcan.apps.api.models.requests import TestCodeRequest
from vulcan.apps.api.models.responses import TestCodeResponse, ErrorResponse


# Configure logger
logger = logging.getLogger("vulcan-api")

# Create router
router = APIRouter()


@router.post(
    "/run",
    response_model=TestCodeResponse,
    responses={
        400: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
    summary="Run tests on code",
    description="Run tests on the provided code",
)
async def run_tests(
    request: TestCodeRequest,
    api_key: str = Depends(get_api_key),
):
    """
    Run tests on the provided code.
    
    Args:
        request: Test code request
        api_key: API key for authentication
        
    Returns:
        Test code response
    """
    try:
        logger.info(f"Received test code request with {len(request.code_content)} files")
        
        # Initialize workflow
        workflow = TestingWorkflow()
        
        # Execute workflow
        result = await workflow.execute_async(
            code_content=request.code_content,
            generate_coverage=request.generate_coverage,
        )
        
        # Create response
        response = TestCodeResponse(
            success=result.success,
            process_id=result.process_id,
            test_results=[
                {
                    "name": test_result.test_case.name,
                    "passed": test_result.passed,
                    "execution_time": test_result.execution_time,
                    "error_message": test_result.error_message,
                }
                for test_result in result.test_results
            ],
            coverage=(
                {
                    "line": result.coverage.line_coverage,
                    "branch": result.coverage.branch_coverage,
                    "function": result.coverage.function_coverage,
                }
                if result.coverage
                else None
            ),
            error_message=result.error_message,
        )
        
        return response
    
    except Exception as e:
        logger.error(f"Error running tests: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error running tests: {str(e)}",
        )