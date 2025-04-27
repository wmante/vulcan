# Vulcan

Vulcan is an autonomous coding agent that can write, test, and deploy code based on user instructions. It integrates with GitHub for version control and CI/CD pipelines, providing a complete end-to-end solution for autonomous software development.

## Project Structure

This project follows a monorepo structure with the following main directories:

- `apps/`: Contains all user-facing applications
- `packages/`: Contains shared internal packages
- `tools/`: Contains development and build tools
- `config/`: Contains configuration files
- `docs/`: Contains documentation
- `tests/`: Contains test suites
- `scripts/`: Contains utility scripts

## Getting Started

### Prerequisites

- Python 3.9 or higher
- [Poetry](https://python-poetry.org/docs/#installation) for dependency management

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/vulcan.git
   cd vulcan
   ```

2. Install dependencies:
   ```bash
   poetry install
   ```

### Development

1. Activate the virtual environment:
   ```bash
   poetry shell
   ```

2. Run tests:
   ```bash
   pytest
   ```

3. Check code formatting:
   ```bash
   black .
   isort .
   ```

4. Run linting:
   ```bash
   flake8 packages/ tests/
   ```

5. Run type checking:
   ```bash
   mypy packages/
   ```

## Core Components

### Core Domain Model

The core domain model consists of three main aggregates:

1. **CodeGeneration**: Handles the generation of code based on user requirements.
2. **CodeTesting**: Manages the testing of generated code.
3. **CodeDeployment**: Handles the deployment of code to GitHub repositories.

### Architecture

The project follows Clean Architecture principles with the following layers:

1. **Presentation Layer**: Handles user interactions.
2. **Application Layer**: Orchestrates workflows and use cases.
3. **Domain Layer**: Contains the core business logic and domain models.
4. **Infrastructure Layer**: Provides implementations for external services and tools.

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
