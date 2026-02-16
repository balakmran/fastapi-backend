# Contributing Guide

Thank you for your interest in contributing to the QuoinAPI project! This
guide will help you set up your development environment and understand the
project structure.

## 🛠️ Prerequisites

Ensure you have the following tools installed:

- [Git](https://git-scm.com/) - Version control
- [Python 3.12+](https://www.python.org/downloads/)
- [uv](https://github.com/astral-sh/uv) - Python package manager
- [just](https://github.com/casey/just) - Command runner
- [OrbStack](https://orbstack.dev/) (recommended) or
  [Docker Desktop](https://www.docker.com/products/docker-desktop/)

## ⚡️ Development Setup

```bash
# 1. Clone the Repository
git clone https://github.com/balakmran/quoin-api.git
cd quoin-api

# 2. Setup Project
# Use `just` to install dependencies and pre-commit hooks.
just setup

# 3. Start the Database
# Start the PostgreSQL database container in the background.
just db

# 4. Apply Migrations
# Run Alembic migrations to set up the database schema.
just migrate-up

# 5. Run the Server
# Start the local development server with auto-reload enabled.
just run
```

## 📸 Application Home Page

After running the server, you can visit [http://127.0.0.1:8000](http://127.0.0.1:8000) to see the application's home page:

![QuoinAPI Home Page](../assets/images/quoin-api-homepage.png)

This confirms the application is running correctly. The page includes:

- **Project Status**: Real-time health indicators for the application and its
  dependencies.
- **Quick Links**: Direct access to API documentation and other resources.

## 🤝 Contribution Workflow

### Fixing Bugs

1.  **Check Issues**: Look for existing issues to avoid duplicates.
2.  **Create Issue**: If not found, create a new issue describing the bug with
    reproduction steps.
3.  **Create Branch**: `git checkout -b fix/issue-number-short-description`
4.  **Reproduce**: Write a test case in `tests/` that reproduces the bug (it
    should fail).
5.  **Fix**: Implement the fix until the test passes.
6.  **Verify**: Run `just check` to ensure no regressions.
7.  **Submit PR**: Open a Pull Request referencing the issue.

### Adding Features

1.  **Propose**: Open a discussion or issue to propose the feature.
2.  **Create Branch**: `git checkout -b feat/short-description`
3.  **Document**: Update `docs/` if the feature involves user-facing changes.
4.  **Implement**: Write tests and code. Follow TDD where possible.
5.  **Verify**: Run `just check`.
6.  **Submit PR**: Open a Pull Request.

### 💎 Coding Standards

We enforce strict coding standards to maintain a high-quality codebase.

- **AI Agents**: Please refer to [AGENTS.md](AGENTS.md) for detailed
  architectural and stylistic rules.
- **Style**: We use [Ruff](https://github.com/astral-sh/ruff) for formatting and
  linting.
- **Types**: 100% type coverage is required.
- **Commits**: Follow
  [Conventional Commits](https://www.conventionalcommits.org/).

## 📜 Development Commands

We use `just` to manage project commands. Run `just --list` to see all available
commands.

| Command                  | Description                                               |
| :----------------------- | :-------------------------------------------------------- |
| `just setup`             | Setup project (install dependencies and pre-commit hooks) |
| `just install`           | Install project dependencies using `uv`                   |
| `just run`               | Start the local development server with auto-reload       |
| `just db`                | Start only the PostgreSQL database container              |
| `just up`                | Start all Docker containers (App + DB)                    |
| `just down`              | Stop and remove all Docker containers                     |
| `just check`             | Run all quality checks (format, lint, typecheck, test)    |
| `just clean`             | Remove build artifacts and cache directories              |
| `just pi`                | Install pre-commit hooks (`prek install`)                 |
| `just pr`                | Run pre-commit hooks on all files (`prek run`)            |
| `just docb`              | Build documentation (`docs-build`)                        |
| `just ds`                | Serve documentation locally (`docs-serve`)                |
| `just migrate-gen "msg"` | Generate a new Alembic migration with a message           |
| `just migrate-up`        | Apply all pending migrations                              |
| `just bump part`         | Bump version (part: `patch`, `minor`, `major`)            |
| `just tag`               | Create and push git tag for current version               |

## 📁 Project Structure

```
.
├── alembic/            # Database migrations
├── app/
│   ├── core/           # Core configuration (config, logging)
│   ├── db/             # Database session and base models
│   ├── modules/        # Feature modules (e.g., user)
│   └── main.py         # Application entry point
├── docs/               # Project documentation (MkDocs)
├── tests/              # Test suite
├── docker-compose.yml  # Docker services configuration
├── Dockerfile          # Application container definition
├── justfile            # Command runner configuration
├── pyproject.toml      # Project dependencies and tool config
└── README.md           # Project documentation
```

## 🧪 Quality Assurance

This project maintains high code quality standards using:

- **Ruff**: For extremely fast linting and formatting.
- **ty**: For static type checking.
- **Pytest**: For testing.

Run all checks with a single command:

```bash
just check
```
