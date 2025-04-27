"""
Unit tests for the Vulcan CLI test command.
"""
import argparse
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from vulcan.apps.cli.commands.test_command import test_command


@patch("vulcan.apps.cli.commands.test_command.Path")
@patch("vulcan.apps.cli.commands.test_command.print_error")
def test_test_command_path_not_exists(mock_print_error, mock_path):
    """Test that test_command checks if the code path exists."""
    # Set up mocks
    mock_args = MagicMock()
    mock_args.path = "path/to/code"
    
    mock_path_instance = MagicMock()
    mock_path_instance.exists.return_value = False
    mock_path.return_value = mock_path_instance
    
    # Call test_command
    result = test_command(mock_args)
    
    # Assert that Path was called with the correct arguments
    mock_path.assert_called_once_with("path/to/code")
    
    # Assert that exists was called
    mock_path_instance.exists.assert_called_once()
    
    # Assert that print_error was called with the expected message
    mock_print_error.assert_called_once_with(f"Path does not exist: {mock_path_instance}")
    
    # Assert that the result is 1 (failure)
    assert result == 1


@patch("vulcan.apps.cli.commands.test_command.Path")
@patch("vulcan.apps.cli.commands.test_command.print_info")
@patch("vulcan.apps.cli.commands.test_command.print_success")
@patch("vulcan.apps.cli.commands.test_command.print_table")
@patch("vulcan.apps.cli.commands.test_command.TestingWorkflow")
def test_test_command_success_all_passed(
    mock_workflow_class,
    mock_print_table,
    mock_print_success,
    mock_print_info,
    mock_path,
):
    """Test that test_command executes successfully when all tests pass."""
    # Set up mocks
    mock_args = MagicMock()
    mock_args.path = "path/to/code"
    mock_args.coverage = False
    
    mock_path_instance = MagicMock()
    mock_path_instance.exists.return_value = True
    mock_path.return_value = mock_path_instance
    
    mock_workflow = MagicMock()
    mock_workflow_class.return_value = mock_workflow
    
    mock_test_case = MagicMock()
    mock_test_case.name = "test_add"
    
    mock_test_result = MagicMock()
    mock_test_result.test_case = mock_test_case
    mock_test_result.passed = True
    mock_test_result.execution_time = 0.001
    
    mock_result = MagicMock()
    mock_result.success = True
    mock_result.test_results = [mock_test_result]
    mock_result.coverage = None
    mock_workflow.execute.return_value = mock_result
    
    # Call test_command
    result = test_command(mock_args)
    
    # Assert that the workflow was executed with the correct arguments
    mock_workflow.execute.assert_called_once_with(mock_path_instance, generate_coverage=False)
    
    # Assert that the success message was printed
    mock_print_success.assert_called_once_with("Testing completed successfully!")
    
    # Assert that print_table was called with the expected arguments
    mock_print_table.assert_called_once()
    
    # Assert that the result is 0 (success)
    assert result == 0


@patch("vulcan.apps.cli.commands.test_command.Path")
@patch("vulcan.apps.cli.commands.test_command.print_info")
@patch("vulcan.apps.cli.commands.test_command.print_success")
@patch("vulcan.apps.cli.commands.test_command.print_table")
@patch("vulcan.apps.cli.commands.test_command.TestingWorkflow")
def test_test_command_success_with_failures(
    mock_workflow_class,
    mock_print_table,
    mock_print_success,
    mock_print_info,
    mock_path,
):
    """Test that test_command returns failure when some tests fail."""
    # Set up mocks
    mock_args = MagicMock()
    mock_args.path = "path/to/code"
    mock_args.coverage = False
    
    mock_path_instance = MagicMock()
    mock_path_instance.exists.return_value = True
    mock_path.return_value = mock_path_instance
    
    mock_workflow = MagicMock()
    mock_workflow_class.return_value = mock_workflow
    
    mock_test_case1 = MagicMock()
    mock_test_case1.name = "test_add"
    
    mock_test_case2 = MagicMock()
    mock_test_case2.name = "test_subtract"
    
    mock_test_result1 = MagicMock()
    mock_test_result1.test_case = mock_test_case1
    mock_test_result1.passed = True
    mock_test_result1.execution_time = 0.001
    
    mock_test_result2 = MagicMock()
    mock_test_result2.test_case = mock_test_case2
    mock_test_result2.passed = False
    mock_test_result2.execution_time = 0.001
    
    mock_result = MagicMock()
    mock_result.success = True
    mock_result.test_results = [mock_test_result1, mock_test_result2]
    mock_result.coverage = None
    mock_workflow.execute.return_value = mock_result
    
    # Call test_command
    result = test_command(mock_args)
    
    # Assert that the workflow was executed with the correct arguments
    mock_workflow.execute.assert_called_once_with(mock_path_instance, generate_coverage=False)
    
    # Assert that the success message was printed
    mock_print_success.assert_called_once_with("Testing completed successfully!")
    
    # Assert that print_table was called with the expected arguments
    mock_print_table.assert_called_once()
    
    # Assert that the result is 1 (failure)
    assert result == 1


@patch("vulcan.apps.cli.commands.test_command.Path")
@patch("vulcan.apps.cli.commands.test_command.print_info")
@patch("vulcan.apps.cli.commands.test_command.print_success")
@patch("vulcan.apps.cli.commands.test_command.print_table")
@patch("vulcan.apps.cli.commands.test_command.TestingWorkflow")
def test_test_command_success_with_coverage(
    mock_workflow_class,
    mock_print_table,
    mock_print_success,
    mock_print_info,
    mock_path,
):
    """Test that test_command prints coverage information when available."""
    # Set up mocks
    mock_args = MagicMock()
    mock_args.path = "path/to/code"
    mock_args.coverage = True
    
    mock_path_instance = MagicMock()
    mock_path_instance.exists.return_value = True
    mock_path.return_value = mock_path_instance
    
    mock_workflow = MagicMock()
    mock_workflow_class.return_value = mock_workflow
    
    mock_test_case = MagicMock()
    mock_test_case.name = "test_add"
    
    mock_test_result = MagicMock()
    mock_test_result.test_case = mock_test_case
    mock_test_result.passed = True
    mock_test_result.execution_time = 0.001
    
    mock_coverage = MagicMock()
    mock_coverage.line_coverage = 90.0
    mock_coverage.branch_coverage = 80.0
    mock_coverage.function_coverage = 100.0
    
    mock_result = MagicMock()
    mock_result.success = True
    mock_result.test_results = [mock_test_result]
    mock_result.coverage = mock_coverage
    mock_workflow.execute.return_value = mock_result
    
    # Call test_command
    result = test_command(mock_args)
    
    # Assert that the workflow was executed with the correct arguments
    mock_workflow.execute.assert_called_once_with(mock_path_instance, generate_coverage=True)
    
    # Assert that the success message was printed
    mock_print_success.assert_called_once_with("Testing completed successfully!")
    
    # Assert that print_table was called with the expected arguments
    mock_print_table.assert_called_once()
    
    # Assert that print_info was called with the coverage information
    assert mock_print_info.call_count >= 4
    mock_print_info.assert_any_call("Coverage Summary:")
    mock_print_info.assert_any_call("  Line coverage: 90.0%")
    mock_print_info.assert_any_call("  Branch coverage: 80.0%")
    mock_print_info.assert_any_call("  Function coverage: 100.0%")
    
    # Assert that the result is 0 (success)
    assert result == 0


@patch("vulcan.apps.cli.commands.test_command.Path")
@patch("vulcan.apps.cli.commands.test_command.print_info")
@patch("vulcan.apps.cli.commands.test_command.print_error")
@patch("vulcan.apps.cli.commands.test_command.TestingWorkflow")
def test_test_command_workflow_failure(
    mock_workflow_class,
    mock_print_error,
    mock_print_info,
    mock_path,
):
    """Test that test_command handles workflow failure correctly."""
    # Set up mocks
    mock_args = MagicMock()
    mock_args.path = "path/to/code"
    mock_args.coverage = False
    
    mock_path_instance = MagicMock()
    mock_path_instance.exists.return_value = True
    mock_path.return_value = mock_path_instance
    
    mock_workflow = MagicMock()
    mock_workflow_class.return_value = mock_workflow
    
    mock_result = MagicMock()
    mock_result.success = False
    mock_result.error_message = "Failed to run tests"
    mock_workflow.execute.return_value = mock_result
    
    # Call test_command
    result = test_command(mock_args)
    
    # Assert that the workflow was executed with the correct arguments
    mock_workflow.execute.assert_called_once_with(mock_path_instance, generate_coverage=False)
    
    # Assert that the error message was printed
    mock_print_error.assert_called_once_with("Testing failed: Failed to run tests")
    
    # Assert that the result is 1 (failure)
    assert result == 1


@patch("vulcan.apps.cli.commands.test_command.print_error")
def test_test_command_exception(mock_print_error):
    """Test that test_command handles exceptions correctly."""
    # Set up mocks
    mock_args = MagicMock()
    mock_args.path = "path/to/code"
    
    # Call test_command with an argument that will cause an exception
    # (since we haven't mocked all the dependencies)
    result = test_command(mock_args)
    
    # Assert that the error message was printed
    mock_print_error.assert_called_once()
    
    # Assert that the result is 1 (failure)
    assert result == 1