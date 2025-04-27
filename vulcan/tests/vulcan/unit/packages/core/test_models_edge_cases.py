"""
Unit tests for edge cases in the domain models of the vulcan_core package.
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


def test_requirements_empty_constraints_examples():
    """Test creating a Requirements instance with empty constraints and examples."""
    requirements = Requirements(
        description="Create a simple Python function to add two numbers",
    )

    assert requirements.description == "Create a simple Python function to add two numbers"
    assert len(requirements.constraints) == 0
    assert len(requirements.examples) == 0


def test_code_artifact_empty_metadata():
    """Test creating a CodeArtifact instance with empty metadata."""
    artifact = CodeArtifact(
        content="def add(a, b): return a + b",
        file_path="add.py",
        language="python",
    )

    assert artifact.content == "def add(a, b): return a + b"
    assert artifact.file_path == "add.py"
    assert artifact.language == "python"
    assert len(artifact.metadata) == 0


def test_code_metadata_empty_additional_info():
    """Test creating a CodeMetadata instance with empty additional_info."""
    metadata = CodeMetadata(
        generation_timestamp="2023-06-01T12:00:00Z",
        model_used="gpt-4",
        prompt_tokens=100,
        completion_tokens=50,
    )

    assert metadata.generation_timestamp == "2023-06-01T12:00:00Z"
    assert metadata.model_used == "gpt-4"
    assert metadata.prompt_tokens == 100
    assert metadata.completion_tokens == 50
    assert len(metadata.additional_info) == 0


def test_code_generation_empty_artifacts():
    """Test creating a CodeGeneration instance with empty artifacts."""
    requirements = Requirements(
        description="Create a simple Python function to add two numbers",
    )
    code_gen = CodeGeneration(requirements=requirements)

    assert code_gen.requirements.description == "Create a simple Python function to add two numbers"
    assert len(code_gen.artifacts) == 0
    assert code_gen.metadata is None
    assert code_gen.status == CodeStatus.NOT_STARTED


def test_code_generation_failed_status():
    """Test a CodeGeneration instance with failed status."""
    requirements = Requirements(
        description="Create a simple Python function to add two numbers",
    )
    code_gen = CodeGeneration(requirements=requirements)
    code_gen.status = CodeStatus.FAILED

    assert code_gen.status == CodeStatus.FAILED


def test_test_case_mocked():
    """Test creating a TestCase instance with is_mocked=True."""
    test_case = TestCase(
        name="test_add_positive_numbers",
        description="Test adding two positive numbers",
        input_data={"a": "2", "b": "3"},
        expected_output={"result": "5"},
        is_mocked=True,
    )

    assert test_case.name == "test_add_positive_numbers"
    assert test_case.description == "Test adding two positive numbers"
    assert test_case.input_data == {"a": "2", "b": "3"}
    assert test_case.expected_output == {"result": "5"}
    assert test_case.is_mocked is True


def test_test_result_with_error():
    """Test creating a TestResult instance with an error message."""
    test_case = TestCase(
        name="test_add_positive_numbers",
        description="Test adding two positive numbers",
        input_data={"a": "2", "b": "3"},
        expected_output={"result": "5"},
    )
    test_result = TestResult(
        test_case=test_case,
        passed=False,
        actual_output={},
        error_message="TypeError: unsupported operand type(s) for +: 'int' and 'str'",
        execution_time=0.001,
    )

    assert test_result.test_case.name == "test_add_positive_numbers"
    assert test_result.passed is False
    assert test_result.actual_output == {}
    assert test_result.error_message == "TypeError: unsupported operand type(s) for +: 'int' and 'str'"
    assert test_result.execution_time == 0.001


def test_test_coverage_empty_file_coverage():
    """Test creating a TestCoverage instance with empty file_coverage."""
    coverage = TestCoverage(
        line_coverage=80.0,
        branch_coverage=75.0,
        function_coverage=90.0,
    )

    assert coverage.line_coverage == 80.0
    assert coverage.branch_coverage == 75.0
    assert coverage.function_coverage == 90.0
    assert len(coverage.file_coverage) == 0


def test_code_testing_empty_test_cases_results():
    """Test creating a CodeTesting instance with empty test_cases and test_results."""
    code_testing = CodeTesting()

    assert len(code_testing.test_cases) == 0
    assert len(code_testing.test_results) == 0
    assert code_testing.coverage is None
    assert code_testing.status == CodeStatus.NOT_STARTED


def test_code_testing_failed_status():
    """Test a CodeTesting instance with failed status."""
    code_testing = CodeTesting()
    code_testing.status = CodeStatus.FAILED

    assert code_testing.status == CodeStatus.FAILED


def test_deployment_config_empty_additional_config():
    """Test creating a DeploymentConfig instance with empty additional_config."""
    config = DeploymentConfig(
        environment="production",
        repository_url="https://github.com/example/repo.git",
        branch="main",
        commit_message="Add function to add two numbers",
    )

    assert config.environment == "production"
    assert config.repository_url == "https://github.com/example/repo.git"
    assert config.branch == "main"
    assert config.commit_message == "Add function to add two numbers"
    assert len(config.additional_config) == 0


def test_deployment_status_empty_logs():
    """Test creating a DeploymentStatus instance with empty logs."""
    status = DeploymentStatus(
        status=CodeStatus.NOT_STARTED,
    )

    assert status.status == CodeStatus.NOT_STARTED
    assert status.deployment_url is None
    assert len(status.logs) == 0
    assert status.error_message is None


def test_deployment_status_with_error():
    """Test creating a DeploymentStatus instance with an error message."""
    status = DeploymentStatus(
        status=CodeStatus.FAILED,
        error_message="Failed to push to remote repository",
    )

    assert status.status == CodeStatus.FAILED
    assert status.error_message == "Failed to push to remote repository"


def test_release_metadata_empty_additional_info():
    """Test creating a ReleaseMetadata instance with empty additional_info."""
    metadata = ReleaseMetadata(
        version="1.0.0",
        release_notes="Initial release with add function",
        release_timestamp="2023-06-01T14:00:00Z",
        author="AI Agent",
    )

    assert metadata.version == "1.0.0"
    assert metadata.release_notes == "Initial release with add function"
    assert metadata.release_timestamp == "2023-06-01T14:00:00Z"
    assert metadata.author == "AI Agent"
    assert len(metadata.additional_info) == 0


def test_code_deployment_without_metadata():
    """Test creating a CodeDeployment instance without metadata."""
    config = DeploymentConfig(
        environment="production",
        repository_url="https://github.com/example/repo.git",
        branch="main",
        commit_message="Add function to add two numbers",
    )
    status = DeploymentStatus(
        status=CodeStatus.NOT_STARTED,
    )
    code_deployment = CodeDeployment(
        config=config,
        status=status,
    )

    assert code_deployment.config.environment == "production"
    assert code_deployment.status.status == CodeStatus.NOT_STARTED
    assert code_deployment.metadata is None