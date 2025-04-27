"""
Command implementation for generating code.
"""
import argparse
import os
import uuid
from pathlib import Path
from typing import Dict, Any

from vulcan.apps.cli.utils.console import print_error, print_info, print_success
from vulcan.src.packages.core.models.code_generation import CodeGeneration, Requirements
from vulcan.src.packages.llm_services.services.code_generator import CodeGenerator
from vulcan.src.packages.workflow_engine.workflows.code_generation_flow import CodeGenerationWorkflow


def generate_command(args: argparse.Namespace) -> int:
    """
    Execute the generate command.
    
    Args:
        args: Command line arguments
        
    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    try:
        # Determine output directory
        output_dir = args.output
        if not output_dir:
            from vulcan.apps.cli.config import DEFAULT_OUTPUT_DIR
            
            # Create a unique directory for this generation
            generation_id = str(uuid.uuid4())[:8]
            output_dir = DEFAULT_OUTPUT_DIR / f"generation_{generation_id}"
        else:
            output_dir = Path(output_dir)
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        print_info(f"Generating code based on requirements...")
        print_info(f"Output directory: {output_dir}")
        
        # Create requirements
        requirements = Requirements(description=args.description)
        
        # Initialize code generation workflow
        workflow = CodeGenerationWorkflow()
        
        # Execute workflow
        result = workflow.execute(requirements, output_dir)
        
        if result.success:
            print_success(f"Code generation completed successfully!")
            print_info(f"Generated {len(result.artifacts)} files:")
            
            for artifact in result.artifacts:
                print_info(f"  - {artifact.file_path}")
            
            return 0
        else:
            print_error(f"Code generation failed: {result.error_message}")
            return 1
    
    except Exception as e:
        print_error(f"Error during code generation: {str(e)}")
        return 1