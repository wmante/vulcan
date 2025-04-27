"""
Unit tests for the domain models in the vulcan_core package.
"""
import pytest

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../../src')))

from core.vulcan_core.models import (
    CodeArtifact,
    CodeDeployment,
    CodeGeneration,
    CodeMetadata,
    CodeStatus,
    CodeTesting,
    DeploymentConfig,
    DeploymentStatus,
    ReleaseMetadata,
    Requirements,
    TestCase,
    TestCoverage,
    TestResult,
)


def test_requirements_creation():
    """Test creating a Requirements instance."""
    requirements = Requirements(
        description="Create a simple Python function to add two numbers",
        constraints=["Must include type hints", "Must include docstring"],
        examples=["add(2, 3) -> 5", "add(-1, 1) -> 0"],
    )

    assert requirements.description == "Create a simple Python function to add two numbers"
    assert len(requirements.constraints) == 2
    assert "Must include type hints" in requirements.constraints
    assert len(requirements.examples) == 2
    assert "add(2, 3) -> 5" in requirements.examples


def test_code_generation_workflow():
    """Test the code generation workflow."""
    # Create requirements
    requirements = Requirements(
        description="Create a simple Python function to add two numbers",
    )

    # Initialize code generation
    code_gen = CodeGeneration(requirements=requirements)
    assert code_gen.status == CodeStatus.NOT_STARTED

    # Update status to in progress
    code_gen.status = CodeStatus.IN_PROGRESS
    assert code_gen.status == CodeStatus.IN_PROGRESS

    # Add a code artifact
    artifact = CodeArtifact(
        content="def add(a: int, b: int) -> int:\n    \"\"\"Add two numbers.\"\"\"\n    return a + b",
        file_path="add.py",
        language="python",
    )
    code_gen.artifacts.append(artifact)
    assert len(code_gen.artifacts) == 1

    # Add metadata
    metadata = CodeMetadata(
        generation_timestamp="2023-06-01T12:00:00Z",
        model_used="gpt-4",
        prompt_tokens=100,
        completion_tokens=50,
    )
    code_gen.metadata = metadata
    assert code_gen.metadata.model_used == "gpt-4"

    # Complete code generation
    code_gen.status = CodeStatus.COMPLETED
    assert code_gen.status == CodeStatus.COMPLETED


def test_code_testing_workflow():
    """Test the code testing workflow."""
    # Create a test case
    test_case = TestCase(
        name="test_add_positive_numbers",
        description="Test adding two positive numbers",
        input_data={"a": "2", "b": "3"},
        expected_output={"result": "5"},
    )

    # Initialize code testing
    code_testing = CodeTesting(test_cases=[test_case])
    assert code_testing.status == CodeStatus.NOT_STARTED
    assert len(code_testing.test_cases) == 1

    # Update status to in progress
    code_testing.status = CodeStatus.IN_PROGRESS
    assert code_testing.status == CodeStatus.IN_PROGRESS

    # Add a test result
    test_result = TestResult(
        test_case=test_case,
        passed=True,
        actual_output={"result": "5"},
        execution_time=0.001,
    )
    code_testing.test_results.append(test_result)
    assert len(code_testing.test_results) == 1
    assert code_testing.test_results[0].passed

    # Add coverage information
    coverage = TestCoverage(
        line_coverage=100.0,
        branch_coverage=100.0,
        function_coverage=100.0,
        file_coverage={"add.py": 100.0},
    )
    code_testing.coverage = coverage
    assert code_testing.coverage.line_coverage == 100.0

    # Complete code testing
    code_testing.status = CodeStatus.COMPLETED
    assert code_testing.status == CodeStatus.COMPLETED


def test_code_deployment_workflow():
    """Test the code deployment workflow."""
    # Create deployment configuration
    config = DeploymentConfig(
        environment="production",
        repository_url="https://github.com/example/repo.git",
        branch="main",
        commit_message="Add function to add two numbers",
    )

    # Initialize deployment status
    status = DeploymentStatus(
        status=CodeStatus.NOT_STARTED,
    )

    # Initialize code deployment
    code_deployment = CodeDeployment(
        config=config,
        status=status,
    )
    assert code_deployment.status.status == CodeStatus.NOT_STARTED

    # Update status to in progress
    code_deployment.status.status = CodeStatus.IN_PROGRESS
    assert code_deployment.status.status == CodeStatus.IN_PROGRESS

    # Add logs
    code_deployment.status.logs.append("Cloning repository...")
    code_deployment.status.logs.append("Committing changes...")
    code_deployment.status.logs.append("Pushing to remote...")
    assert len(code_deployment.status.logs) == 3

    # Complete deployment
    code_deployment.status.status = CodeStatus.COMPLETED
    code_deployment.status.deployment_url = "https://github.com/example/repo/commit/abc123"
    assert code_deployment.status.status == CodeStatus.COMPLETED
    assert code_deployment.status.deployment_url == "https://github.com/example/repo/commit/abc123"

    # Add release metadata
    metadata = ReleaseMetadata(
        version="1.0.0",
        release_notes="Initial release with add function",
        release_timestamp="2023-06-01T14:00:00Z",
        author="AI Agent",
    )
    code_deployment.metadata = metadata
    assert code_deployment.metadata.version == "1.0.0"
