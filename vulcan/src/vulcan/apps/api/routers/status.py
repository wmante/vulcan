"""
Router for status endpoints.
"""
import logging
from fastapi import APIRouter, Depends, HTTPException, status

from vulcan.apps.api.middleware.auth import get_api_key
from vulcan.apps.api.models.requests import StatusRequest
from vulcan.apps.api.models.responses import StatusResponse, ErrorResponse


# Configure logger
logger = logging.getLogger("vulcan-api")

# Create router
router = APIRouter()


@router.get(
    "/{process_id}",
    response_model=StatusResponse,
    responses={
        400: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
    summary="Check process status",
    description="Check the status of a code generation, testing, or deployment process",
)
async def get_status(
    process_id: str,
    api_key: str = Depends(get_api_key),
):
    """
    Check the status of a process.
    
    Args:
        process_id: ID of the process to check
        api_key: API key for authentication
        
    Returns:
        Status response
    """
    try:
        logger.info(f"Received status request for process: {process_id}")
        
        # Initialize state manager
        state_manager = WorkflowStateManager()
        
        # Get process state
        state = await state_manager.get_state_async(process_id)
        
        if not state:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Process not found: {process_id}",
            )
        
        # Create response
        response = StatusResponse(
            process_id=state.process_id,
            process_type=state.process_type,
            status=state.status.name.lower(),
            start_time=state.start_time,
            end_time=state.end_time,
            steps=[
                {
                    "name": step.name,
                    "status": step.status.name.lower(),
                    "start_time": step.start_time,
                    "end_time": step.end_time,
                }
                for step in state.steps
            ],
            artifacts=state.artifacts,
            errors=state.errors,
        )
        
        return response
    
    except HTTPException:
        raise
    
    except Exception as e:
        logger.error(f"Error checking status: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error checking status: {str(e)}",
        )


@router.post(
    "/",
    response_model=StatusResponse,
    responses={
        400: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
    summary="Check process status",
    description="Check the status of a code generation, testing, or deployment process",
)
async def check_status(
    request: StatusRequest,
    api_key: str = Depends(get_api_key),
):
    """
    Check the status of a process.
    
    Args:
        request: Status request
        api_key: API key for authentication
        
    Returns:
        Status response
    """
    return await get_status(request.process_id, api_key)