"""
Router for deployment endpoints.
"""
import logging
from fastapi import APIRouter, Depends, HTTPException, status

from vulcan.apps.api.middleware.auth import get_api_key
from vulcan.apps.api.models.requests import DeployCodeRequest
from vulcan.apps.api.models.responses import DeployCodeResponse, ErrorResponse


# Configure logger
logger = logging.getLogger("vulcan-api")

# Create router
router = APIRouter()


@router.post(
    "/deploy",
    response_model=DeployCodeResponse,
    responses={
        400: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
    summary="Deploy code to GitHub",
    description="Deploy the provided code to a GitHub repository",
)
async def deploy_code(
    request: DeployCodeRequest,
    api_key: str = Depends(get_api_key),
):
    """
    Deploy the provided code to a GitHub repository.
    
    Args:
        request: Deploy code request
        api_key: API key for authentication
        
    Returns:
        Deploy code response
    """
    try:
        logger.info(
            f"Received deploy code request to {request.repository_url} "
            f"(branch: {request.branch}) with {len(request.code_content)} files"
        )
        
        # Initialize workflow
        workflow = DeploymentWorkflow()
        
        # Execute workflow
        result = await workflow.execute_async(
            code_content=request.code_content,
            repository_url=request.repository_url,
            branch=request.branch,
            commit_message=request.commit_message,
        )
        
        # Create response
        response = DeployCodeResponse(
            success=result.success,
            process_id=result.process_id,
            deployment_url=result.deployment_url,
            logs=result.logs,
            error_message=result.error_message,
        )
        
        return response
    
    except Exception as e:
        logger.error(f"Error deploying code: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deploying code: {str(e)}",
        )