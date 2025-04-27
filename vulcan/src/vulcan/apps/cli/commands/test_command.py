"""
Command implementation for testing code.
"""
import argparse
from pathlib import Path

from vulcan.apps.cli.utils.console import print_error, print_info, print_success, print_table
from vulcan.src.packages.testing_framework.services.test_runner import TestRunner
from vulcan.src.packages.workflow_engine.workflows.testing_flow import TestingWorkflow


def test_command(args: argparse.Namespace) -> int:
    """
    Execute the test command.
    
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
        
        print_info(f"Running tests for code at: {code_path}")
        
        # Initialize testing workflow
        workflow = TestingWorkflow()
        
        # Execute workflow
        result = workflow.execute(code_path, generate_coverage=args.coverage)
        
        if result.success:
            print_success(f"Testing completed successfully!")
            
            # Print test results
            headers = ["Test", "Status", "Duration (s)"]
            rows = []
            
            for test_result in result.test_results:
                status = "✓ Passed" if test_result.passed else "✗ Failed"
                rows.append([
                    test_result.test_case.name,
                    status,
                    f"{test_result.execution_time:.3f}"
                ])
            
            print_table(headers, rows, "Test Results")
            
            # Print coverage information if available
            if result.coverage:
                print_info(f"Coverage Summary:")
                print_info(f"  Line coverage: {result.coverage.line_coverage:.1f}%")
                print_info(f"  Branch coverage: {result.coverage.branch_coverage:.1f}%")
                print_info(f"  Function coverage: {result.coverage.function_coverage:.1f}%")
            
            # Determine exit code based on test results
            if all(result.passed for result in result.test_results):
                return 0
            else:
                return 1
        else:
            print_error(f"Testing failed: {result.error_message}")
            return 1
    
    except Exception as e:
        print_error(f"Error during testing: {str(e)}")
        return 1