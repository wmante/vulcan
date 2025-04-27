"""
API client for the Vulcan web application.
"""
import json
import logging
from typing import Dict, List, Optional, Any, Union

import requests
from requests.exceptions import RequestException


logger = logging.getLogger("vulcan-web")


class VulcanAPIClient:
    """Client for interacting with the Vulcan API."""
    
    def __init__(self, api_url: str, api_key: str):
        """
        Initialize the API client.
        
        Args:
            api_url: Base URL of the API
            api_key: API key for authentication
        """
        self.api_url = api_url.rstrip("/")
        self.api_key = api_key
        self.headers = {
            "X-API-Key": api_key,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
    
    def check_health(self) -> bool:
        """
        Check if the API is healthy.
        
        Returns:
            True if the API is healthy, False otherwise
        """
        try:
            response = requests.get(
                f"{self.api_url}/health",
                headers=self.headers,
                timeout=5,
            )
            return response.status_code == 200
        except RequestException as e:
            logger.error(f"Error checking API health: {str(e)}")
            return False
    
    def generate_code(
        self,
        description: str,
        constraints: Optional[List[str]] = None,
        examples: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Generate code based on requirements.
        
        Args:
            description: Description of the code to generate
            constraints: Constraints for the generated code
            examples: Examples of expected behavior
            
        Returns:
            Response from the API
        """
        try:
            payload = {
                "description": description,
                "constraints": constraints or [],
                "examples": examples or [],
            }
            
            response = requests.post(
                f"{self.api_url}/api/v1/code-generation/generate",
                headers=self.headers,
                json=payload,
                timeout=60,
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Error generating code: {response.text}")
                return {
                    "success": False,
                    "error_message": f"API error: {response.status_code} - {response.text}",
                }
        
        except RequestException as e:
            logger.error(f"Error generating code: {str(e)}")
            return {
                "success": False,
                "error_message": f"Request error: {str(e)}",
            }
    
    def run_tests(
        self,
        code_content: Dict[str, str],
        generate_coverage: bool = False,
    ) -> Dict[str, Any]:
        """
        Run tests on code.
        
        Args:
            code_content: Dictionary mapping file paths to code content
            generate_coverage: Whether to generate coverage report
            
        Returns:
            Response from the API
        """
        try:
            payload = {
                "code_content": code_content,
                "generate_coverage": generate_coverage,
            }
            
            response = requests.post(
                f"{self.api_url}/api/v1/testing/run",
                headers=self.headers,
                json=payload,
                timeout=60,
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Error running tests: {response.text}")
                return {
                    "success": False,
                    "error_message": f"API error: {response.status_code} - {response.text}",
                }
        
        except RequestException as e:
            logger.error(f"Error running tests: {str(e)}")
            return {
                "success": False,
                "error_message": f"Request error: {str(e)}",
            }
    
    def deploy_code(
        self,
        code_content: Dict[str, str],
        repository_url: str,
        branch: str = "main",
        commit_message: str = "Deploy code via Vulcan API",
    ) -> Dict[str, Any]:
        """
        Deploy code to GitHub.
        
        Args:
            code_content: Dictionary mapping file paths to code content
            repository_url: GitHub repository URL
            branch: Branch to deploy to
            commit_message: Commit message
            
        Returns:
            Response from the API
        """
        try:
            payload = {
                "code_content": code_content,
                "repository_url": repository_url,
                "branch": branch,
                "commit_message": commit_message,
            }
            
            response = requests.post(
                f"{self.api_url}/api/v1/deployment/deploy",
                headers=self.headers,
                json=payload,
                timeout=60,
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Error deploying code: {response.text}")
                return {
                    "success": False,
                    "error_message": f"API error: {response.status_code} - {response.text}",
                }
        
        except RequestException as e:
            logger.error(f"Error deploying code: {str(e)}")
            return {
                "success": False,
                "error_message": f"Request error: {str(e)}",
            }
    
    def check_status(self, process_id: str) -> Dict[str, Any]:
        """
        Check the status of a process.
        
        Args:
            process_id: ID of the process to check
            
        Returns:
            Response from the API
        """
        try:
            response = requests.get(
                f"{self.api_url}/api/v1/status/{process_id}",
                headers=self.headers,
                timeout=30,
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Error checking status: {response.text}")
                return {
                    "success": False,
                    "error_message": f"API error: {response.status_code} - {response.text}",
                }
        
        except RequestException as e:
            logger.error(f"Error checking status: {str(e)}")
            return {
                "success": False,
                "error_message": f"Request error: {str(e)}",
            }