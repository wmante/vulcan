"""
Console output utilities for the Vulcan CLI.
"""
import sys
from typing import Any, List, Optional


def print_banner() -> None:
    """Print the Vulcan CLI banner."""
    banner = """
    __      __    _                
    \ \    / /   | |               
     \ \  / /   _| | ___ __ _ _ __  
      \ \/ / | | | |/ __/ _` | '_ \ 
       \  /| |_| | | (_| (_| | | | |
        \/  \__,_|_|\___\__,_|_| |_|
                                    
    Autonomous Coding Agent
    """
    print(banner)


def print_success(message: str) -> None:
    """
    Print a success message.
    
    Args:
        message: The message to print
    """
    print(f"\033[92m✓ {message}\033[0m")


def print_error(message: str) -> None:
    """
    Print an error message.
    
    Args:
        message: The message to print
    """
    print(f"\033[91m✗ {message}\033[0m", file=sys.stderr)


def print_warning(message: str) -> None:
    """
    Print a warning message.
    
    Args:
        message: The message to print
    """
    print(f"\033[93m! {message}\033[0m")


def print_info(message: str) -> None:
    """
    Print an info message.
    
    Args:
        message: The message to print
    """
    print(f"\033[94m> {message}\033[0m")


def print_table(headers: List[str], rows: List[List[Any]], title: Optional[str] = None) -> None:
    """
    Print a table.
    
    Args:
        headers: The table headers
        rows: The table rows
        title: Optional title for the table
    """
    if not rows:
        return
    
    # Calculate column widths
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))
    
    # Print title if provided
    if title:
        print(f"\n{title}")
        print("-" * len(title))
    
    # Print headers
    header_row = " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
    print(header_row)
    print("-" * len(header_row))
    
    # Print rows
    for row in rows:
        row_str = " | ".join(str(cell).ljust(col_widths[i]) for i, cell in enumerate(row))
        print(row_str)


def print_progress(current: int, total: int, prefix: str = "", suffix: str = "", length: int = 50) -> None:
    """
    Print a progress bar.
    
    Args:
        current: Current progress
        total: Total progress
        prefix: Prefix string
        suffix: Suffix string
        length: Character length of the progress bar
    """
    percent = float(current) * 100 / total
    filled_length = int(length * current // total)
    bar = "█" * filled_length + "-" * (length - filled_length)
    print(f"\r{prefix} |{bar}| {percent:.1f}% {suffix}", end="\r")
    if current == total:
        print()