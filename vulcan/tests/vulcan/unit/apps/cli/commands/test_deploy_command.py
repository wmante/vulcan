"""
Unit tests for the Vulcan CLI deploy command.
"""
import argparse
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from vulcan.apps.cli.commands.deploy_command import deploy_command


@patch("vulcan.apps.cli.commands.deploy_command.Path")
@patch("vulcan.apps.cli.commands.deploy_command.print_error")
def test_deploy_command_path_not_exists(mock_print_error, mock_path):
    """Test that deploy_command checks if the code path exists."""
    # Set up mocks
    mock_args = MagicMock()
    mock_args.path = "path/to/code"
    mock_args.repo = "https://github.com/example/repo.git"
    
    mock_path_instance = MagicMock()
    mock_path_instance.exists.return_value = False
    mock_path.return_value = mock_path_instance
    
    # Call deploy_command
    result = deploy_command(mock_args)
    
    # Assert that Path was called with the correct arguments
    mock_path.assert_called_once_with("path/to/code")
    
    # Assert that exists was called
    mock_path_instance.exists.assert_called_once()
    
    # Assert that print_error was called with the expected message
    mock_print_error.assert_called_once_with(f"Path does not exist: {mock_path_instance}")
    
    # Assert that the result is 1 (failure)
    assert result == 1


@patch("vulcan.apps.cli.commands.deploy_command.Path")
@patch("vulcan.apps.cli.commands.deploy_command.print_error")
def test_deploy_command_no_repo_url(mock_print_error, mock_path):
    """Test that deploy_command checks if the repository URL is provided."""
    # Set up mocks
    mock_args = MagicMock()
    mock_args.path = "path/to/code"
    mock_args.repo = None
    
    mock_path_instance = MagicMock()
    mock_path_instance.exists.return_value = True
    mock_path.return_value = mock_path_instance
    
    # Call deploy_command
    result = deploy_command(mock_args)
    
    # Assert that print_error was called with the expected message
    mock_print_error.assert_called_once_with("Repository URL is required")
    
    # Assert that the result is 1 (failure)
    assert result == 1


@patch("vulcan.apps.cli.commands.deploy_command.Path")
@patch("vulcan.apps.cli.commands.deploy_command.print_info")
@patch("vulcan.apps.cli.commands.deploy_command.print_success")
@patch("vulcan.apps.cli.commands.deploy_command.DeploymentWorkflow")
def test_deploy_command_success(
    mock_workflow_class,
    mock_print_success,
    mock_print_info,
    mock_path,
):
    """Test that deploy_command executes successfully."""
    # Set up mocks
    mock_args = MagicMock()
    mock_args.path = "path/to/code"
    mock_args.repo = "https://github.com/example/repo.git"
    mock_args.branch = "main"
    
    mock_path_instance = MagicMock()
    mock_path_instance.exists.return_value = True
    mock_path.return_value = mock_path_instance
    
    mock_workflow = MagicMock()
    mock_workflow_class.return_value = mock_workflow
    
    mock_result = MagicMock()
    mock_result.success = True
    mock_result.deployment_url = "https://github.com/example/repo/commit/abc123"
    mock_workflow.execute.return_value = mock_result
    
    # Call deploy_command
    result = deploy_command(mock_args)
    
    # Assert that the workflow was executed with the correct arguments
    mock_workflow.execute.assert_called_once_with(
        code_path=mock_path_instance,
        repository_url="https://github.com/example/repo.git",
        branch="main",
    )
    
    # Assert that the success message was printed
    mock_print_success.assert_called_once_with("Deployment completed successfully!")
    
    # Assert that the deployment URL was printed
    mock_print_info.assert_any_call("Deployment URL: https://github.com/example/repo/commit/abc123")
    
    # Assert that the result is 0 (success)
    assert result == 0


@patch("vulcan.apps.cli.commands.deploy_command.Path")
@patch("vulcan.apps.cli.commands.deploy_command.print_info")
@patch("vulcan.apps.cli.commands.deploy_command.print_error")
@patch("vulcan.apps.cli.commands.deploy_command.DeploymentWorkflow")
def test_deploy_command_failure(
    mock_workflow_class,
    mock_print_error,
    mock_print_info,
    mock_path,
):
    """Test that deploy_command handles workflow failure correctly."""
    # Set up mocks
    mock_args = MagicMock()
    mock_args.path = "path/to/code"
    mock_args.repo = "https://github.com/example/repo.git"
    mock_args.branch = "main"
    
    mock_path_instance = MagicMock()
    mock_path_instance.exists.return_value = True
    mock_path.return_value = mock_path_instance
    
    mock_workflow = MagicMock()
    mock_workflow_class.return_value = mock_workflow
    
    mock_result = MagicMock()
    mock_result.success = False
    mock_result.error_message = "Failed to deploy code"
    mock_result.logs = ["Cloning repository...", "Error: Authentication failed"]
    mock_workflow.execute.return_value = mock_result
    
    # Call deploy_command
    result = deploy_command(mock_args)
    
    # Assert that the workflow was executed with the correct arguments
    mock_workflow.execute.assert_called_once_with(
        code_path=mock_path_instance,
        repository_url="https://github.com/example/repo.git",
        branch="main",
    )
    
    # Assert that the error message was printed
    mock_print_error.assert_called_once_with("Deployment failed: Failed to deploy code")
    
    # Assert that the logs were printed
    mock_print_info.assert_any_call("Deployment logs:")
    mock_print_info.assert_any_call("  Cloning repository...")
    mock_print_info.assert_any_call("  Error: Authentication failed")
    
    # Assert that the result is 1 (failure)
    assert result == 1


@patch("vulcan.apps.cli.commands.deploy_command.print_error")
def test_deploy_command_exception(mock_print_error):
    """Test that deploy_command handles exceptions correctly."""
    # Set up mocks
    mock_args = MagicMock()
    mock_args.path = "path/to/code"
    mock_args.repo = "https://github.com/example/repo.git"
    
    # Call deploy_command with an argument that will cause an exception
    # (since we haven't mocked all the dependencies)
    result = deploy_command(mock_args)
    
    # Assert that the error message was printed
    mock_print_error.assert_called_once()
    
    # Assert that the result is 1 (failure)
    assert result == 1