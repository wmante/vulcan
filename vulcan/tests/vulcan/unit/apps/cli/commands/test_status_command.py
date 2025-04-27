"""
Unit tests for the Vulcan CLI status command.
"""
import argparse
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from vulcan.apps.cli.commands.status_command import status_command
from vulcan.src.packages.core.models.common import CodeStatus


@patch("vulcan.apps.cli.commands.status_command.print_info")
@patch("vulcan.apps.cli.commands.status_command.print_error")
@patch("vulcan.apps.cli.commands.status_command.WorkflowStateManager")
def test_status_command_process_not_found(
    mock_state_manager_class,
    mock_print_error,
    mock_print_info,
):
    """Test that status_command handles the case when the process is not found."""
    # Set up mocks
    mock_args = MagicMock()
    mock_args.id = "process-id"
    
    mock_state_manager = MagicMock()
    mock_state_manager.get_state.return_value = None
    mock_state_manager_class.return_value = mock_state_manager
    
    # Call status_command
    result = status_command(mock_args)
    
    # Assert that WorkflowStateManager was created
    mock_state_manager_class.assert_called_once()
    
    # Assert that get_state was called with the correct arguments
    mock_state_manager.get_state.assert_called_once_with("process-id")
    
    # Assert that print_error was called with the expected message
    mock_print_error.assert_called_once_with("No process found with ID: process-id")
    
    # Assert that the result is 1 (failure)
    assert result == 1


@patch("vulcan.apps.cli.commands.status_command.print_info")
@patch("vulcan.apps.cli.commands.status_command.print_table")
@patch("vulcan.apps.cli.commands.status_command.WorkflowStateManager")
def test_status_command_basic_info(
    mock_state_manager_class,
    mock_print_table,
    mock_print_info,
):
    """Test that status_command prints basic process information."""
    # Set up mocks
    mock_args = MagicMock()
    mock_args.id = "process-id"
    
    mock_state = MagicMock()
    mock_state.process_type = "code_generation"
    mock_state.status = CodeStatus.COMPLETED
    mock_state.start_time = "2023-06-01T12:00:00Z"
    mock_state.end_time = "2023-06-01T12:05:00Z"
    mock_state.steps = []
    mock_state.artifacts = []
    mock_state.errors = []
    
    mock_state_manager = MagicMock()
    mock_state_manager.get_state.return_value = mock_state
    mock_state_manager_class.return_value = mock_state_manager
    
    # Call status_command
    result = status_command(mock_args)
    
    # Assert that WorkflowStateManager was created
    mock_state_manager_class.assert_called_once()
    
    # Assert that get_state was called with the correct arguments
    mock_state_manager.get_state.assert_called_once_with("process-id")
    
    # Assert that print_info was called with the expected messages
    mock_print_info.assert_any_call("Checking status for process: process-id")
    mock_print_info.assert_any_call("Process Type: code_generation")
    mock_print_info.assert_any_call("Status: COMPLETED")
    mock_print_info.assert_any_call("Started: 2023-06-01T12:00:00Z")
    mock_print_info.assert_any_call("Completed: 2023-06-01T12:05:00Z")
    
    # Assert that the result is 0 (success)
    assert result == 0


@patch("vulcan.apps.cli.commands.status_command.print_info")
@patch("vulcan.apps.cli.commands.status_command.print_table")
@patch("vulcan.apps.cli.commands.status_command.WorkflowStateManager")
def test_status_command_with_steps(
    mock_state_manager_class,
    mock_print_table,
    mock_print_info,
):
    """Test that status_command prints process steps."""
    # Set up mocks
    mock_args = MagicMock()
    mock_args.id = "process-id"
    
    mock_step1 = MagicMock()
    mock_step1.name = "Parse Requirements"
    mock_step1.status = CodeStatus.COMPLETED
    mock_step1.start_time = "2023-06-01T12:00:00Z"
    mock_step1.end_time = "2023-06-01T12:01:00Z"
    
    mock_step2 = MagicMock()
    mock_step2.name = "Generate Code"
    mock_step2.status = CodeStatus.IN_PROGRESS
    mock_step2.start_time = "2023-06-01T12:01:00Z"
    mock_step2.end_time = None
    
    mock_state = MagicMock()
    mock_state.process_type = "code_generation"
    mock_state.status = CodeStatus.IN_PROGRESS
    mock_state.start_time = "2023-06-01T12:00:00Z"
    mock_state.end_time = None
    mock_state.steps = [mock_step1, mock_step2]
    mock_state.artifacts = []
    mock_state.errors = []
    
    mock_state_manager = MagicMock()
    mock_state_manager.get_state.return_value = mock_state
    mock_state_manager_class.return_value = mock_state_manager
    
    # Call status_command
    result = status_command(mock_args)
    
    # Assert that print_table was called with the expected arguments
    mock_print_table.assert_called_once()
    args, kwargs = mock_print_table.call_args
    assert args[0] == ["Step", "Status", "Started", "Completed"]
    assert len(args[1]) == 2
    assert kwargs["title"] == "Process Steps"
    
    # Assert that the result is 0 (success)
    assert result == 0


@patch("vulcan.apps.cli.commands.status_command.print_info")
@patch("vulcan.apps.cli.commands.status_command.WorkflowStateManager")
def test_status_command_with_artifacts(
    mock_state_manager_class,
    mock_print_info,
):
    """Test that status_command prints process artifacts."""
    # Set up mocks
    mock_args = MagicMock()
    mock_args.id = "process-id"
    
    mock_artifact1 = MagicMock()
    mock_artifact1.name = "add.py"
    mock_artifact1.path = "/output/add.py"
    
    mock_artifact2 = MagicMock()
    mock_artifact2.name = "test_add.py"
    mock_artifact2.path = "/output/test_add.py"
    
    mock_state = MagicMock()
    mock_state.process_type = "code_generation"
    mock_state.status = CodeStatus.COMPLETED
    mock_state.start_time = "2023-06-01T12:00:00Z"
    mock_state.end_time = "2023-06-01T12:05:00Z"
    mock_state.steps = []
    mock_state.artifacts = [mock_artifact1, mock_artifact2]
    mock_state.errors = []
    
    mock_state_manager = MagicMock()
    mock_state_manager.get_state.return_value = mock_state
    mock_state_manager_class.return_value = mock_state_manager
    
    # Call status_command
    result = status_command(mock_args)
    
    # Assert that print_info was called with the expected messages
    mock_print_info.assert_any_call("Artifacts:")
    mock_print_info.assert_any_call("  - add.py: /output/add.py")
    mock_print_info.assert_any_call("  - test_add.py: /output/test_add.py")
    
    # Assert that the result is 0 (success)
    assert result == 0


@patch("vulcan.apps.cli.commands.status_command.print_info")
@patch("vulcan.apps.cli.commands.status_command.print_error")
@patch("vulcan.apps.cli.commands.status_command.WorkflowStateManager")
def test_status_command_with_errors(
    mock_state_manager_class,
    mock_print_error,
    mock_print_info,
):
    """Test that status_command prints process errors."""
    # Set up mocks
    mock_args = MagicMock()
    mock_args.id = "process-id"
    
    mock_state = MagicMock()
    mock_state.process_type = "code_generation"
    mock_state.status = CodeStatus.FAILED
    mock_state.start_time = "2023-06-01T12:00:00Z"
    mock_state.end_time = "2023-06-01T12:05:00Z"
    mock_state.steps = []
    mock_state.artifacts = []
    mock_state.errors = ["Failed to parse requirements", "Invalid syntax in generated code"]
    
    mock_state_manager = MagicMock()
    mock_state_manager.get_state.return_value = mock_state
    mock_state_manager_class.return_value = mock_state_manager
    
    # Call status_command
    result = status_command(mock_args)
    
    # Assert that print_error was called with the expected messages
    mock_print_error.assert_any_call("Errors:")
    mock_print_error.assert_any_call("  - Failed to parse requirements")
    mock_print_error.assert_any_call("  - Invalid syntax in generated code")
    
    # Assert that the result is 0 (success)
    assert result == 0


@patch("vulcan.apps.cli.commands.status_command.print_error")
def test_status_command_exception(mock_print_error):
    """Test that status_command handles exceptions correctly."""
    # Set up mocks
    mock_args = MagicMock()
    mock_args.id = "process-id"
    
    # Call status_command with an argument that will cause an exception
    # (since we haven't mocked all the dependencies)
    result = status_command(mock_args)
    
    # Assert that the error message was printed
    mock_print_error.assert_called_once()
    
    # Assert that the result is 1 (failure)
    assert result == 1