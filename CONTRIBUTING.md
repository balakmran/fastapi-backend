# Contributing Guide

Thank you for your interest in contributing to the FastAPI Backend project! This guide will help you set up your development environment and understand the project structure.

## 🛠️ Prerequisites

Ensure you have the following tools installed:

- [Git](https://git-scm.com/) - Version control
- [Python 3.12+](https://www.python.org/downloads/)
- [uv](https://github.com/astral-sh/uv) - Python package manager
- [just](https://github.com/casey/just) - Command runner
- [OrbStack](https://orbstack.dev/) (recommended) or [Docker Desktop](https://www.docker.com/products/docker-desktop/)

## ⚡️ Development Setup

1.  **Clone the repository:**

    ```bash
    git clone <repository-url>
    cd fastapi-backend
    ```

2.  **Install dependencies:**

    ```bash
    just install
    ```

3.  **Start the database:**

    ```bash
    just db
    ```

4.  **Apply database migrations:**

    ```bash
    just migrate-up
    ```

5.  **Run the development server:**

    ```bash
    just run
    ```

    The API will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).
    Interactive API docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## 📜 Development Commands

We use `just` to manage project commands. Run `just --list` to see all available commands.

| Command                  | Description                                            |
| :----------------------- | :----------------------------------------------------- |
| `just install`           | Install project dependencies using `uv`                |
| `just run`               | Start the local development server with auto-reload    |
| `just db`                | Start only the PostgreSQL database container           |
| `just up`                | Start all Docker containers (App + DB)                 |
| `just down`              | Stop and remove all Docker containers                  |
| `just check`             | Run all quality checks (format, lint, typecheck, test) |
| `just clean`             | Remove build artifacts and cache directories           |
| `just migrate-gen "msg"` | Generate a new Alembic migration with a message        |
| `just migrate-up`        | Apply all pending migrations                           |
| `just docs-serve`        | Serve the documentation locally                        |

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
