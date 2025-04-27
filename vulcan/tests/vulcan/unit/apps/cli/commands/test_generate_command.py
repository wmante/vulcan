"""
Unit tests for the Vulcan CLI generate command.
"""
import argparse
import os
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from vulcan.apps.cli.commands.generate_command import generate_command


@patch("vulcan.apps.cli.commands.generate_command.os.makedirs")
@patch("vulcan.apps.cli.commands.generate_command.print_info")
@patch("vulcan.apps.cli.commands.generate_command.print_success")
@patch("vulcan.apps.cli.commands.generate_command.Requirements")
@patch("vulcan.apps.cli.commands.generate_command.CodeGenerationWorkflow")
def test_generate_command_success(
    mock_workflow_class,
    mock_requirements_class,
    mock_print_success,
    mock_print_info,
    mock_makedirs,
):
    """Test that generate_command executes successfully."""
    # Set up mocks
    mock_args = MagicMock()
    mock_args.description = "Create a function to add two numbers"
    mock_args.output = "output_dir"
    
    mock_requirements = MagicMock()
    mock_requirements_class.return_value = mock_requirements
    
    mock_workflow = MagicMock()
    mock_workflow_class.return_value = mock_workflow
    
    mock_result = MagicMock()
    mock_result.success = True
    mock_result.artifacts = [MagicMock(file_path="add.py")]
    mock_workflow.execute.return_value = mock_result
    
    # Call generate_command
    result = generate_command(mock_args)
    
    # Assert that the output directory was created
    mock_makedirs.assert_called_once_with(Path("output_dir"), exist_ok=True)
    
    # Assert that Requirements was created with the correct arguments
    mock_requirements_class.assert_called_once_with(description="Create a function to add two numbers")
    
    # Assert that CodeGenerationWorkflow was created
    mock_workflow_class.assert_called_once()
    
    # Assert that the workflow was executed with the correct arguments
    mock_workflow.execute.assert_called_once_with(mock_requirements, Path("output_dir"))
    
    # Assert that the success message was printed
    mock_print_success.assert_called_once_with("Code generation completed successfully!")
    
    # Assert that the result is 0 (success)
    assert result == 0


@patch("vulcan.apps.cli.commands.generate_command.os.makedirs")
@patch("vulcan.apps.cli.commands.generate_command.print_info")
@patch("vulcan.apps.cli.commands.generate_command.print_error")
@patch("vulcan.apps.cli.commands.generate_command.Requirements")
@patch("vulcan.apps.cli.commands.generate_command.CodeGenerationWorkflow")
def test_generate_command_failure(
    mock_workflow_class,
    mock_requirements_class,
    mock_print_error,
    mock_print_info,
    mock_makedirs,
):
    """Test that generate_command handles failure correctly."""
    # Set up mocks
    mock_args = MagicMock()
    mock_args.description = "Create a function to add two numbers"
    mock_args.output = "output_dir"
    
    mock_requirements = MagicMock()
    mock_requirements_class.return_value = mock_requirements
    
    mock_workflow = MagicMock()
    mock_workflow_class.return_value = mock_workflow
    
    mock_result = MagicMock()
    mock_result.success = False
    mock_result.error_message = "Failed to generate code"
    mock_workflow.execute.return_value = mock_result
    
    # Call generate_command
    result = generate_command(mock_args)
    
    # Assert that the output directory was created
    mock_makedirs.assert_called_once_with(Path("output_dir"), exist_ok=True)
    
    # Assert that Requirements was created with the correct arguments
    mock_requirements_class.assert_called_once_with(description="Create a function to add two numbers")
    
    # Assert that CodeGenerationWorkflow was created
    mock_workflow_class.assert_called_once()
    
    # Assert that the workflow was executed with the correct arguments
    mock_workflow.execute.assert_called_once_with(mock_requirements, Path("output_dir"))
    
    # Assert that the error message was printed
    mock_print_error.assert_called_once_with("Code generation failed: Failed to generate code")
    
    # Assert that the result is 1 (failure)
    assert result == 1


@patch("vulcan.apps.cli.commands.generate_command.uuid.uuid4")
@patch("vulcan.apps.cli.commands.generate_command.DEFAULT_OUTPUT_DIR", Path("/default/output"))
@patch("vulcan.apps.cli.commands.generate_command.os.makedirs")
@patch("vulcan.apps.cli.commands.generate_command.print_info")
@patch("vulcan.apps.cli.commands.generate_command.Requirements")
@patch("vulcan.apps.cli.commands.generate_command.CodeGenerationWorkflow")
def test_generate_command_default_output_dir(
    mock_workflow_class,
    mock_requirements_class,
    mock_print_info,
    mock_makedirs,
    mock_uuid4,
):
    """Test that generate_command uses the default output directory when none is specified."""
    # Set up mocks
    mock_args = MagicMock()
    mock_args.description = "Create a function to add two numbers"
    mock_args.output = None
    
    mock_uuid4.return_value = MagicMock(hex="abcd1234")
    
    mock_requirements = MagicMock()
    mock_requirements_class.return_value = mock_requirements
    
    mock_workflow = MagicMock()
    mock_workflow_class.return_value = mock_workflow
    
    mock_result = MagicMock()
    mock_result.success = True
    mock_result.artifacts = []
    mock_workflow.execute.return_value = mock_result
    
    # Call generate_command
    result = generate_command(mock_args)
    
    # Assert that the output directory was created
    expected_output_dir = Path("/default/output/generation_abcd1234")
    mock_makedirs.assert_called_once_with(expected_output_dir, exist_ok=True)
    
    # Assert that the workflow was executed with the correct arguments
    mock_workflow.execute.assert_called_once_with(mock_requirements, expected_output_dir)
    
    # Assert that the result is 0 (success)
    assert result == 0


@patch("vulcan.apps.cli.commands.generate_command.print_error")
def test_generate_command_exception(mock_print_error):
    """Test that generate_command handles exceptions correctly."""
    # Set up mocks
    mock_args = MagicMock()
    mock_args.description = "Create a function to add two numbers"
    mock_args.output = "output_dir"
    
    # Call generate_command with an argument that will cause an exception
    # (since we haven't mocked all the dependencies)
    result = generate_command(mock_args)
    
    # Assert that the error message was printed
    mock_print_error.assert_called_once()
    
    # Assert that the result is 1 (failure)
    assert result == 1