## API Documentation

The Vulcan API provides endpoints for code generation, testing, and deployment.


## Core Components

### Core Domain Model

The core domain model consists of three main aggregates:

1. **CodeGeneration**: Handles the generation of code based on user requirements.
2. **CodeTesting**: Manages the testing of generated code.
3. **CodeDeployment**: Handles the deployment of code to GitHub repositories.

### Architecture

The project follows Clean Architecture principles with the following layers:

1. **Presentation Layer** (in `src/apps/`): Handles user interactions via CLI, API, and Web interfaces.
2. **Application Layer**: Orchestrates workflows and use cases.
3. **Domain Layer**: Contains the core business logic and domain models.
4. **Infrastructure Layer**: Provides implementations for external services and tools.

## Getting Started

### Prerequisites

- Python 3.12 or higher
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

3. Activate the virtual environment:
   ```bash
   poetry shell
   ```

## Running the Application

Vulcan provides three different interfaces that you can use based on your preferences:

### CLI Application
### API Server
```
bash vulcan-api
```
### Web Interface

```
bash vulcan-web
```
### Environment Setup

1. Create a `.env` file in the project root:
   ```
   VULCAN_API_KEY=your_api_key_here
   VULCAN_API_URL=https://api.vulcan.dev
   VULCAN_ENV=development
   GITHUB_TOKEN=your_github_token
   ```

### Authentication

All API requests require an API key to be included in the Authorization header:
