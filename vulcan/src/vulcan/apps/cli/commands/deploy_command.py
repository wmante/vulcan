"""
Command implementation for deploying code.
"""
import argparse
from pathlib import Path

from vulcan.apps.cli.utils.console import print_error, print_info, print_success
from vulcan.src.packages.github_integration.services.repository_service import RepositoryService
from vulcan.src.packages.workflow_engine.workflows.deployment_flow import DeploymentWorkflow


def deploy_command(args: argparse.Namespace) -> int:
    """
    Execute the deploy command.
    
    Args:
        args: Command line arguments
        
    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    try:
        code_path = Path(args.path)
        
        if not code_path.exists():
            print_error(f"Path does not exist: {code_path}")
            return 1
        
        # Get repository URL
        repo_url = args.repo
        if not repo_url:
            print_error("Repository URL is required")
            return 1
        
        branch = args.branch
        
        print_info(f"Deploying code from {code_path} to {repo_url} (branch: {branch})...")
        
        # Initialize deployment workflow
        workflow = DeploymentWorkflow()
        
        # Execute workflow
        result = workflow.execute(
            code_path=code_path,
            repository_url=repo_url,
            branch=branch,
        )
        
        if result.success:
            print_success(f"Deployment completed successfully!")
            
            if result.deployment_url:
                print_info(f"Deployment URL: {result.deployment_url}")
            
            return 0
        else:
            print_error(f"Deployment failed: {result.error_message}")
            
            # Print logs if available
            if result.logs:
                print_info("Deployment logs:")
                for log in result.logs:
                    print_info(f"  {log}")
            
            return 1
    
    except Exception as e:
        print_error(f"Error during deployment: {str(e)}")
        return 1