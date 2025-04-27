"""
Command implementation for checking status.
"""
import argparse
import json
from pathlib import Path
from typing import Dict, Any, List

from vulcan.apps.cli.utils.console import print_error, print_info, print_success, print_table
from vulcan.src.packages.core.models.common import CodeStatus
from vulcan.src.packages.workflow_engine.state.workflow_state import WorkflowStateManager


def status_command(args: argparse.Namespace) -> int:
    """
    Execute the status command.
    
    Args:
        args: Command line arguments
        
    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    try:
        process_id = args.id
        
        print_info(f"Checking status for process: {process_id}")
        
        # Initialize workflow state manager
        state_manager = WorkflowStateManager()
        
        # Get process state
        state = state_manager.get_state(process_id)
        
        if not state:
            print_error(f"No process found with ID: {process_id}")
            return 1
        
        # Print process information
        print_info(f"Process Type: {state.process_type}")
        print_info(f"Status: {state.status.name}")
        print_info(f"Started: {state.start_time}")
        
        if state.end_time:
            print_info(f"Completed: {state.end_time}")
        
        # Print steps
        if state.steps:
            headers = ["Step", "Status", "Started", "Completed"]
            rows = []
            
            for step in state.steps:
                status_str = step.status.name
                if step.status == CodeStatus.COMPLETED:
                    status_str = f"✓ {status_str}"
                elif step.status == CodeStatus.FAILED:
                    status_str = f"✗ {status_str}"
                elif step.status == CodeStatus.IN_PROGRESS:
                    status_str = f"⟳ {status_str}"
                
                rows.append([
                    step.name,
                    status_str,
                    step.start_time,
                    step.end_time or ""
                ])
            
            print_table(headers, rows, "Process Steps")
        
        # Print artifacts if available
        if state.artifacts:
            print_info("Artifacts:")
            for artifact in state.artifacts:
                print_info(f"  - {artifact.name}: {artifact.path}")
        
        # Print errors if any
        if state.errors:
            print_error("Errors:")
            for error in state.errors:
                print_error(f"  - {error}")
        
        return 0
    
    except Exception as e:
        print_error(f"Error checking status: {str(e)}")
        return 1