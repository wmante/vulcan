"""
Entry point for the Vulcan CLI application.
"""
import argparse
import sys
from typing import List, Optional

from vulcan.apps.cli.commands.generate_command import generate_command
from vulcan.apps.cli.commands.test_command import test_command
from vulcan.apps.cli.commands.deploy_command import deploy_command
from vulcan.apps.cli.commands.status_command import status_command
from vulcan.apps.cli.utils.console import print_banner, print_error, print_success
from vulcan.apps.cli.config import CLI_VERSION


def create_parser() -> argparse.ArgumentParser:
    """Create the command line argument parser."""
    parser = argparse.ArgumentParser(
        description="Vulcan - Autonomous Coding Agent",
        epilog="For more information, visit: https://github.com/yourusername/vulcan",
    )
    
    parser.add_argument(
        "--version", action="version", version=f"Vulcan CLI v{CLI_VERSION}"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Generate command
    generate_parser = subparsers.add_parser(
        "generate", help="Generate code based on requirements"
    )
    generate_parser.add_argument(
        "description", help="Description of the code to generate"
    )
    generate_parser.add_argument(
        "--output", "-o", help="Output directory for generated code"
    )
    
    # Test command
    test_parser = subparsers.add_parser("test", help="Run tests on generated code")
    test_parser.add_argument(
        "path", help="Path to the code to test"
    )
    test_parser.add_argument(
        "--coverage", "-c", action="store_true", help="Generate coverage report"
    )
    
    # Deploy command
    deploy_parser = subparsers.add_parser("deploy", help="Deploy code to GitHub")
    deploy_parser.add_argument(
        "path", help="Path to the code to deploy"
    )
    deploy_parser.add_argument(
        "--repo", "-r", help="GitHub repository URL"
    )
    deploy_parser.add_argument(
        "--branch", "-b", default="main", help="Branch to deploy to"
    )
    
    # Status command
    status_parser = subparsers.add_parser(
        "status", help="Check status of code generation, testing, or deployment"
    )
    status_parser.add_argument(
        "id", help="ID of the process to check"
    )
    
    return parser


def main(args: Optional[List[str]] = None) -> int:
    """Main entry point for the CLI application."""
    if args is None:
        args = sys.argv[1:]
    
    parser = create_parser()
    parsed_args = parser.parse_args(args)
    
    if not parsed_args.command:
        print_banner()
        parser.print_help()
        return 0
    
    try:
        if parsed_args.command == "generate":
            return generate_command(parsed_args)
        elif parsed_args.command == "test":
            return test_command(parsed_args)
        elif parsed_args.command == "deploy":
            return deploy_command(parsed_args)
        elif parsed_args.command == "status":
            return status_command(parsed_args)
        else:
            print_error(f"Unknown command: {parsed_args.command}")
            return 1
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())