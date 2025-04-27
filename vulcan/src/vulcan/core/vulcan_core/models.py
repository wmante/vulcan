"""
Domain models for the Vulcan autonomous coding agent.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional


class CodeStatus(Enum):
    """Status of code generation, testing, or deployment."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Requirements:
    """User requirements for code generation."""
    description: str
    constraints: List[str] = field(default_factory=list)
    examples: List[str] = field(default_factory=list)


@dataclass
class CodeArtifact:
    """Generated code artifact."""
    content: str
    file_path: str
    language: str
    metadata: Dict[str, str] = field(default_factory=dict)


@dataclass
class CodeMetadata:
    """Metadata for generated code."""
    generation_timestamp: str
    model_used: str
    prompt_tokens: int
    completion_tokens: int
    additional_info: Dict[str, str] = field(default_factory=dict)


@dataclass
class CodeGeneration:
    """Code generation aggregate."""
    requirements: Requirements
    artifacts: List[CodeArtifact] = field(default_factory=list)
    metadata: Optional[CodeMetadata] = None
    status: CodeStatus = CodeStatus.NOT_STARTED


@dataclass
class TestCase:
    """Test case for code testing."""
    name: str
    description: str
    input_data: Dict[str, str]
    expected_output: Dict[str, str]
    is_mocked: bool = False


@dataclass
class TestResult:
    """Result of a test execution."""
    test_case: TestCase
    passed: bool
    actual_output: Dict[str, str]
    error_message: Optional[str] = None
    execution_time: float = 0.0


@dataclass
class TestCoverage:
    """Test coverage information."""
    line_coverage: float
    branch_coverage: float
    function_coverage: float
    file_coverage: Dict[str, float] = field(default_factory=dict)


@dataclass
class CodeTesting:
    """Code testing aggregate."""
    test_cases: List[TestCase] = field(default_factory=list)
    test_results: List[TestResult] = field(default_factory=list)
    coverage: Optional[TestCoverage] = None
    status: CodeStatus = CodeStatus.NOT_STARTED


@dataclass
class DeploymentConfig:
    """Configuration for code deployment."""
    environment: str
    repository_url: str
    branch: str
    commit_message: str
    additional_config: Dict[str, str] = field(default_factory=dict)


@dataclass
class DeploymentStatus:
    """Status of code deployment."""
    status: CodeStatus
    deployment_url: Optional[str] = None
    logs: List[str] = field(default_factory=list)
    error_message: Optional[str] = None


@dataclass
class ReleaseMetadata:
    """Metadata for a code release."""
    version: str
    release_notes: str
    release_timestamp: str
    author: str
    additional_info: Dict[str, str] = field(default_factory=dict)


@dataclass
class CodeDeployment:
    """Code deployment aggregate."""
    config: DeploymentConfig
    status: DeploymentStatus
    metadata: Optional[ReleaseMetadata] = None