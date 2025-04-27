"""
FastAPI application entry point for the Vulcan API.
"""
import logging
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from vulcan.apps.api.config import API_VERSION, API_TITLE, API_DESCRIPTION, ALLOWED_ORIGINS
from vulcan.apps.api.middleware.auth import get_api_key, verify_api_key
from vulcan.apps.api.middleware.logging import LoggingMiddleware
from vulcan.apps.api.routers import code_generation, testing, deployment, status

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("vulcan-api")

# Create FastAPI application
app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add logging middleware
app.add_middleware(LoggingMiddleware)

# Include routers
app.include_router(
    code_generation.router,
    prefix="/api/v1/code-generation",
    tags=["Code Generation"],
    dependencies=[Depends(verify_api_key)],
)

app.include_router(
    testing.router,
    prefix="/api/v1/testing",
    tags=["Testing"],
    dependencies=[Depends(verify_api_key)],
)

app.include_router(
    deployment.router,
    prefix="/api/v1/deployment",
    tags=["Deployment"],
    dependencies=[Depends(verify_api_key)],
)

app.include_router(
    status.router,
    prefix="/api/v1/status",
    tags=["Status"],
    dependencies=[Depends(verify_api_key)],
)


@app.get("/", tags=["Health"])
async def root():
    """Health check endpoint."""
    return {"status": "ok", "version": API_VERSION}


@app.get("/health", tags=["Health"])
async def health():
    """Health check endpoint."""
    return {"status": "ok", "version": API_VERSION}


def start():
    """Start the FastAPI application with uvicorn."""
    import uvicorn
    
    uvicorn.run("vulcan.apps.api.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    start()