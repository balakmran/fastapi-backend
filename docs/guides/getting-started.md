# Getting Started

Welcome to the **FastAPI Backend** project! This guide will help you set up your development environment and get the application running locally.

## 🛠️ Prerequisites

Ensure you have the following tools installed:

- **[Git](https://git-scm.com/)**: Version control system.
- **[Python 3.12+](https://www.python.org/downloads/)**: The programming language used.
- **[uv](https://github.com/astral-sh/uv)**: A fast Python package installer and manager.
- **[just](https://github.com/casey/just)**: A handy command runner for project tasks.
- **[Docker](https://www.docker.com/)**: Required for running the database and services.

## ⚡️ Quick Start

Follow these steps to get up and running in minutes.

```bash
# 1. Clone the Repository
git clone https://github.com/balakmran/fastapi-backend.git
cd fastapi-backend

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

The application will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).

- **API Documentation**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Redoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## 📁 Project Structure

Understanding the project layout will help you navigate the codebase.

```plaintext
.
├── app/
│   ├── core/                   # Core configuration (settings, logging, exceptions)
│   ├── db/                     # Database session and base models
│   ├── modules/                # Domain-specific feature modules (e.g., user)
│   │   └── user/               # Example module
│   │       ├── models.py       # database tables
│   │       ├── schemas.py      # Pydantic models
│   │       ├── routes.py       # API endpoints
│   │       └── service.py      # Business logic
│   └── main.py                 # Application entry point
├── tests/                      # Test suite
├── alembic/                    # Database migrations
├── docker-compose.yml          # Local development services
├── justfile                    # Task runner configuration
└── pyproject.toml              # Project dependencies and tool config
```

## ❓ Troubleshooting

### Port Conflicts

If `just run` fails, check if port **8000** is already in use.

```bash
lsof -i :8000
```

### Database Connection

If the app cannot connect to the database:

1. Ensure the Docker container is running: `docker ps`
2. Check logs: `docker compose logs db`
3. Restart the database: `just db`
