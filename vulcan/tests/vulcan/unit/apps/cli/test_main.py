"""
Unit tests for the Vulcan CLI main module.
"""
import argparse
import pytest
from unittest.mock import patch, MagicMock

from vulcan.apps.cli.main import create_parser, main


def test_create_parser():
    """Test that create_parser creates a parser with the expected arguments."""
    parser = create_parser()
    
    # Test that the parser is an ArgumentParser
    assert isinstance(parser, argparse.ArgumentParser)
    
    # Test that the parser has the expected description
    assert parser.description == "Vulcan - Autonomous Coding Agent"
    
    # Test that the parser has the expected subparsers
    subparsers_action = next(action for action in parser._actions if isinstance(action, argparse._SubParsersAction))
    assert "generate" in subparsers_action.choices
    assert "test" in subparsers_action.choices
    assert "deploy" in subparsers_action.choices
    assert "status" in subparsers_action.choices
    
    # Test that the generate subparser has the expected arguments
    generate_parser = subparsers_action.choices["generate"]
    generate_args = {action.dest: action for action in generate_parser._actions}
    assert "description" in generate_args
    assert "output" in generate_args
    
    # Test that the test subparser has the expected arguments
    test_parser = subparsers_action.choices["test"]
    test_args = {action.dest: action for action in test_parser._actions}
    assert "path" in test_args
    assert "coverage" in test_args
    
    # Test that the deploy subparser has the expected arguments
    deploy_parser = subparsers_action.choices["deploy"]
    deploy_args = {action.dest: action for action in deploy_parser._actions}
    assert "path" in deploy_args
    assert "repo" in deploy_args
    assert "branch" in deploy_args
    
    # Test that the status subparser has the expected arguments
    status_parser = subparsers_action.choices["status"]
    status_args = {action.dest: action for action in status_parser._actions}
    assert "id" in status_args


@patch("vulcan.apps.cli.main.print_banner")
@patch("vulcan.apps.cli.main.generate_command")
def test_main_generate_command(mock_generate_command, mock_print_banner):
    """Test that main calls the generate command function."""
    # Set up the mock
    mock_generate_command.return_value = 0
    
    # Call main with generate command
    result = main(["generate", "Create a function to add two numbers"])
    
    # Assert that the generate command function was called
    mock_generate_command.assert_called_once()
    
    # Assert that the result is the return value of the generate command function
    assert result == 0


@patch("vulcan.apps.cli.main.print_banner")
@patch("vulcan.apps.cli.main.test_command")
def test_main_test_command(mock_test_command, mock_print_banner):
    """Test that main calls the test command function."""
    # Set up the mock
    mock_test_command.return_value = 0
    
    # Call main with test command
    result = main(["test", "path/to/code"])
    
    # Assert that the test command function was called
    mock_test_command.assert_called_once()
    
    # Assert that the result is the return value of the test command function
    assert result == 0


@patch("vulcan.apps.cli.main.print_banner")
@patch("vulcan.apps.cli.main.deploy_command")
def test_main_deploy_command(mock_deploy_command, mock_print_banner):
    """Test that main calls the deploy command function."""
    # Set up the mock
    mock_deploy_command.return_value = 0
    
    # Call main with deploy command
    result = main(["deploy", "path/to/code", "--repo", "https://github.com/example/repo.git"])
    
    # Assert that the deploy command function was called
    mock_deploy_command.assert_called_once()
    
    # Assert that the result is the return value of the deploy command function
    assert result == 0


@patch("vulcan.apps.cli.main.print_banner")
@patch("vulcan.apps.cli.main.status_command")
def test_main_status_command(mock_status_command, mock_print_banner):
    """Test that main calls the status command function."""
    # Set up the mock
    mock_status_command.return_value = 0
    
    # Call main with status command
    result = main(["status", "process-id"])
    
    # Assert that the status command function was called
    mock_status_command.assert_called_once()
    
    # Assert that the result is the return value of the status command function
    assert result == 0


@patch("vulcan.apps.cli.main.print_banner")
@patch("vulcan.apps.cli.main.print_error")
def test_main_unknown_command(mock_print_error, mock_print_banner):
    """Test that main handles unknown commands."""
    # Call main with unknown command
    result = main(["unknown"])
    
    # Assert that print_error was called with the expected message
    mock_print_error.assert_called_once_with("Unknown command: unknown")
    
    # Assert that the result is 1 (error)
    assert result == 1


@patch("vulcan.apps.cli.main.print_banner")
@patch("vulcan.apps.cli.main.print_error")
@patch("vulcan.apps.cli.main.generate_command")
def test_main_exception(mock_generate_command, mock_print_error, mock_print_banner):
    """Test that main handles exceptions."""
    # Set up the mock to raise an exception
    mock_generate_command.side_effect = Exception("Test exception")
    
    # Call main with generate command
    result = main(["generate", "Create a function to add two numbers"])
    
    # Assert that print_error was called with the expected message
    mock_print_error.assert_called_once_with("Error: Test exception")
    
    # Assert that the result is 1 (error)
    assert result == 1


@patch("vulcan.apps.cli.main.print_banner")
def test_main_no_command(mock_print_banner):
    """Test that main handles no command."""
    # Call main with no command
    result = main([])
    
    # Assert that print_banner was called
    mock_print_banner.assert_called_once()
    
    # Assert that the result is 0 (success)
    assert result == 0