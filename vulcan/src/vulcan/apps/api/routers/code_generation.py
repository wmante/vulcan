"""
Router for code generation endpoints.
"""
import logging
from fastapi import APIRouter, Depends, HTTPException, status

from vulcan.apps.api.middleware.auth import get_api_key
from vulcan.apps.api.models.requests import GenerateCodeRequest
from vulcan.apps.api.models.responses import GenerateCodeResponse, ErrorResponse
from vulcan.core.vulcan_core.models import Requirements


# Configure logger
logger = logging.getLogger("vulcan-api")

# Create router
router = APIRouter()


@router.post(
    "/generate",
    response_model=GenerateCodeResponse,
    responses={
        400: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
    summary="Generate code based on requirements",
    description="Generate code based on the provided requirements",
)
async def generate_code(
    request: GenerateCodeRequest,
    api_key: str = Depends(get_api_key),
):
    """
    Generate code based on the provided requirements.
    
    Args:
        request: Code generation request
        api_key: API key for authentication
        
    Returns:
        Code generation response
    """
    try:
        logger.info(f"Received code generation request: {request.description}")
        
        # Create requirements
        requirements = Requirements(
            description=request.description,
            constraints=request.constraints or [],
            examples=request.examples or [],
        )
        
        # Initialize workflow
        workflow = CodeGenerationWorkflow()
        
        # Execute workflow
        result = await workflow.execute_async(requirements)
        
        # Create response
        response = GenerateCodeResponse(
            success=result.success,
            process_id=result.process_id,
            artifacts=[
                {
                    "file_path": artifact.file_path,
                    "content": artifact.content,
                    "language": artifact.language,
                    "metadata": artifact.metadata,
                }
                for artifact in result.artifacts
            ],
            error_message=result.error_message,
        )
        
        return response
    
    except Exception as e:
        logger.error(f"Error generating code: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating code: {str(e)}",
        )