"""
Unit tests for the Vulcan CLI console utilities.
"""
import io
import sys
import pytest
from unittest.mock import patch

from vulcan.apps.cli.utils.console import (
    print_banner,
    print_success,
    print_error,
    print_warning,
    print_info,
    print_table,
    print_progress,
)


@patch("sys.stdout", new_callable=io.StringIO)
def test_print_banner(mock_stdout):
    """Test that print_banner prints the expected banner."""
    print_banner()
    
    output = mock_stdout.getvalue()
    
    # Check that the output contains the expected banner
    assert "__      __    _" in output
    assert "Autonomous Coding Agent" in output


@patch("sys.stdout", new_callable=io.StringIO)
def test_print_success(mock_stdout):
    """Test that print_success prints the expected success message."""
    print_success("Test successful")
    
    output = mock_stdout.getvalue()
    
    # Check that the output contains the expected message
    assert "✓ Test successful" in output
    assert "\033[92m" in output  # Green color
    assert "\033[0m" in output  # Reset color


@patch("sys.stderr", new_callable=io.StringIO)
def test_print_error(mock_stderr):
    """Test that print_error prints the expected error message to stderr."""
    print_error("Test error")
    
    output = mock_stderr.getvalue()
    
    # Check that the output contains the expected message
    assert "✗ Test error" in output
    assert "\033[91m" in output  # Red color
    assert "\033[0m" in output  # Reset color


@patch("sys.stdout", new_callable=io.StringIO)
def test_print_warning(mock_stdout):
    """Test that print_warning prints the expected warning message."""
    print_warning("Test warning")
    
    output = mock_stdout.getvalue()
    
    # Check that the output contains the expected message
    assert "! Test warning" in output
    assert "\033[93m" in output  # Yellow color
    assert "\033[0m" in output  # Reset color


@patch("sys.stdout", new_callable=io.StringIO)
def test_print_info(mock_stdout):
    """Test that print_info prints the expected info message."""
    print_info("Test info")
    
    output = mock_stdout.getvalue()
    
    # Check that the output contains the expected message
    assert "> Test info" in output
    assert "\033[94m" in output  # Blue color
    assert "\033[0m" in output  # Reset color


@patch("sys.stdout", new_callable=io.StringIO)
def test_print_table_with_title(mock_stdout):
    """Test that print_table prints the expected table with a title."""
    headers = ["Name", "Age", "City"]
    rows = [
        ["Alice", 30, "New York"],
        ["Bob", 25, "Los Angeles"],
        ["Charlie", 35, "Chicago"],
    ]
    title = "Test Table"
    
    print_table(headers, rows, title)
    
    output = mock_stdout.getvalue()
    
    # Check that the output contains the expected table
    assert title in output
    assert "Name | Age | City" in output
    assert "Alice | 30 | New York" in output
    assert "Bob | 25 | Los Angeles" in output
    assert "Charlie | 35 | Chicago" in output


@patch("sys.stdout", new_callable=io.StringIO)
def test_print_table_without_title(mock_stdout):
    """Test that print_table prints the expected table without a title."""
    headers = ["Name", "Age", "City"]
    rows = [
        ["Alice", 30, "New York"],
        ["Bob", 25, "Los Angeles"],
        ["Charlie", 35, "Chicago"],
    ]
    
    print_table(headers, rows)
    
    output = mock_stdout.getvalue()
    
    # Check that the output contains the expected table
    assert "Name | Age | City" in output
    assert "Alice | 30 | New York" in output
    assert "Bob | 25 | Los Angeles" in output
    assert "Charlie | 35 | Chicago" in output


@patch("sys.stdout", new_callable=io.StringIO)
def test_print_table_empty_rows(mock_stdout):
    """Test that print_table handles empty rows."""
    headers = ["Name", "Age", "City"]
    rows = []
    
    print_table(headers, rows)
    
    output = mock_stdout.getvalue()
    
    # Check that the output is empty
    assert output == ""


@patch("sys.stdout", new_callable=io.StringIO)
def test_print_progress_partial(mock_stdout):
    """Test that print_progress prints the expected progress bar for partial progress."""
    print_progress(50, 100, prefix="Progress:", suffix="Complete", length=20)
    
    output = mock_stdout.getvalue()
    
    # Check that the output contains the expected progress bar
    assert "Progress:" in output
    assert "50.0%" in output
    assert "Complete" in output
    assert "|" in output
    assert "█" in output
    assert "-" in output


@patch("sys.stdout", new_callable=io.StringIO)
def test_print_progress_complete(mock_stdout):
    """Test that print_progress prints the expected progress bar for complete progress."""
    print_progress(100, 100, prefix="Progress:", suffix="Complete", length=20)
    
    output = mock_stdout.getvalue()
    
    # Check that the output contains the expected progress bar
    assert "Progress:" in output
    assert "100.0%" in output
    assert "Complete" in output
    assert "|" in output
    assert "█" in output
    assert "-" not in output  # No dashes when complete