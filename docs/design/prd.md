# Project Requirements Document (PRD)

# FastAPI Backend

| **Field**        | **Value**                                   |
| ---------------- | ------------------------------------------- |
| **Project Name** | FastAPI Backend                             |
| **Status**       | v0.1.0 Complete                             |
| **Owner**        | Balakumaran Manoharan                       |
| **Version**      | 0.1.0                                       |
| **Last Updated** | 2025-11-26                                  |

## 1. Overview

### 1.1. Project Objective

To build a high-performance, scalable REST API backend using a modern, fully-asynchronous Python stack.

**Version 0.1.0 Focus:** Establish the foundational architecture, database integration (`sqlmodel`/`psycopg`), structured logging, and a robust developer experience without the complexity of authentication or background workers.

### 1.2. Guiding Principles

This project prioritizes:

  * **Developer Experience (DX):** A seamless, fast, and automated local development setup.

  * **Robust Design:** Structured logging, exception handling, and containerization.

  * **Modern Tooling:** Use of the latest, high-performance tools (e.g., `uv`, `ruff`, `ty`).

  * **Automated Quality:** Strict linting, formatting, type-checking, and testing enforced by CI.

## 2. Core Technology Stack

The project will be built exclusively with the following technologies.

| **Domain**        | **Technology**                      | **Purpose**                                |
| ----------------- | ----------------------------------- | ------------------------------------------ |
| **Environment**   | `uv`                                | Python venv and package management.        |
| **Framework**     | `fastapi`                           | Core API framework.                        |
| **Server (Dev)**  | `fastapi-cli` (via `fastapi dev`)   | Local development server with live-reload. |
| **Server (Prod)** | `fastapi-cli` (via `fastapi run`)   | Production ASGI server (wraps Uvicorn).    |
| **Database**      | PostgreSQL (v18+)                   | Primary relational database.               |
| **DB Driver**     | `psycopg` (v3)                      | Asynchronous PostgreSQL driver.            |
| **ORM**           | `sqlmodel`                          | Pydantic-based ORM (atop SQLAlchemy).      |
| **Migrations**    | `alembic`                           | Database migrations.                       |
| **Logging**       | `structlog`                         | Structured, JSON-capable logging.          |
| **Code Quality**  | `ruff`, `ty`                        | Linting/formatting and type checking.      |
| **Dev Tooling**   | `just` (Global), `pre-commit`       | Task runner and Git hooks.                 |
| **Documentation** | `mkdocs`, `mkdocstrings`            | Static site generation from code.          |
| **Config**        | `pydantic-settings`                 | Settings management via env variables.     |

## 3. Project Structure

The project *must* adhere to the following directory structure:

```
/
├── .github/workflows/         # CI/CD pipelines (ci.yml)
├── .dockerignore
├── .env.example               # Example for all required env variables
├── .gitignore
├── .pre-commit-config.yaml    # Pre-commit hook definitions
├── .python-version            # Python version specification
├── docker-compose.yml         # Local development environment
├── Dockerfile                 # Production container image
├── justfile                   # Developer task runner (master command list)
├── pyproject.toml             # Project metadata, dependencies, tool configs
├── uv.lock                    # Lock file for reproducible builds
├── README.md                  # Project overview
├── CONTRIBUTING.md            # New developer setup guide
├── CHANGELOG.md               # Version history
├── alembic.ini                # Alembic configuration
├── alembic/                   # Alembic migration scripts
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
├── app/
│   ├── __init__.py
│   ├── main.py                # FastAPI app factory (create_app)
│   ├── api.py                 # API router aggregation
│   ├── core/                  # Core application configuration
│   │   ├── __init__.py
│   │   ├── config.py          # Pydantic settings & env loading
│   │   ├── logging.py         # Structlog configuration
│   │   ├── openapi.py         # OpenAPI schema customization
│   │   ├── exceptions.py      # Custom exception classes
│   │   ├── exception_handlers.py  # Exception handlers
│   │   └── middlewares.py     # Middleware configuration
│   ├── db/                    # Database configuration
│   │   ├── __init__.py
│   │   └── session.py         # Async engine & session
│   └── modules/               # Feature-based modules (singular naming)
│       ├── __init__.py
│       └── user/              # User module
│           ├── __init__.py
│           ├── routes.py      # FastAPI router (/users/)
│           ├── service.py     # Business logic
│           ├── repository.py  # Data access layer
│           ├── schemas.py     # Pydantic models
│           └── models.py      # SQLModel DB models
├── docs/                      # Documentation source files
│   ├── index.md               # Documentation home page
│   ├── CONTRIBUTING.md        # Symlink to root CONTRIBUTING.md
│   ├── design/                # Design documents
│   │   └── prd.md             # Project Requirements Document (Source of Truth)
│   └── stylesheets/
│       └── extra.css          # Custom documentation styles
├── mkdocs.yml                 # MkDocs configuration
└── tests/                     # Pytest tests
    ├── __init__.py
    ├── conftest.py            # Pytest fixtures (e.g., test DB, client)
    ├── test_main.py           # Main application tests
    ├── test_db.py             # Database tests
    ├── core/                  # Core module tests
    │   ├── test_exceptions.py
    │   ├── test_logging.py
    │   ├── test_middlewares.py
    │   └── test_openapi.py
    └── modules/               # Feature module tests
        └── user/
            └── test_routes.py
```

## 4. Developer Experience (DX) & Tooling

### 4.1. Dependency Management (`uv`)

  * Dependencies *must* be managed in `pyproject.toml`.

  * The following dependency groups *must* be used:

      * `[project.dependencies]` (default): Production dependencies (`fastapi`, `sqlmodel`, `fastapi-cli`, `psycopg`, `structlog`, `pydantic-settings`, `alembic`).

      * `[project.optional-dependencies.dev]`: Development tools (`ruff`, `ty`, `pytest`, `pre-commit`). **Note:** `just` is not a project dependency; it must be installed globally (e.g., `brew install just`).

      * `[project.optional-dependencies.docs]`: Documentation tools (`mkdocs`, `mkdocs-material`, `mkdocstrings`).

### 4.2. Task Runner (`justfile`)

  * A `justfile` *must* be provided as the single entry point for all common tasks.

  * It *must* include, at a minimum, the following recipes:

      * `install`: Installs all dependencies using `uv sync --all-groups`.

      * `run`: Runs the local dev server (`fastapi dev ...`).

      * `lint`: Runs `ruff check . --fix`.

      * `format`: Runs `ruff format .`.

      * `typecheck`: Runs `ty .`.

      * `test`: Runs `pytest`.

      * `check`: Runs `format`, `lint`, `typecheck`, and `test` sequentially.

      * `pre-commit-install`: Installs the Git hooks via `pre-commit`.

      * `docs-serve`: Serves the docs site locally.

      * `docs-build`: Builds the static docs site.

      * `migrate-gen msg="<message>"`: Generates a new Alembic migration.

      * `migrate-up`: Applies database migrations.

### 4.3. Contribution Guide (`CONTRIBUTING.md`)

  * This file *must* provide a clear, step-by-step guide for a new developer to set up and run the project locally, referencing the `justfile` commands.

### 4.4. Pre-commit Hooks

  * A `.pre-commit-config.yaml` *must* be configured to run `ruff format`, `ruff check`, and `ty` on every `git commit` to enforce quality *before* code is pushed.

## 5. Functional Requirements

### 5.1. API & Configuration

  * The API *must* load all configuration (e.g., `DATABASE_URL`) from environment variables via `pydantic-settings` (in `app/core/config.py`).

  * A `.env.example` file *must* be provided.

  * **API Versioning:** The API *must* use **Path-Based Versioning**. All API endpoints *must* be prefixed with a version, e.g., `/api/v1/`.

  * The `app/main.py` file *must* be responsible for creating and mounting the top-level versioned routers (e.g., an `api_v1_router` mounted at `/api/v1`).

### 5.2. Database & ORM

  * The system *must* use `sqlmodel` for all data modeling.

  * All database interactions *must* be asynchronous, using `psycopg`'s async engine and sessions.

  * Database schema changes *must* be managed via `alembic` migrations.

### 5.3. Logging

  * `structlog` *must* be configured as the sole logging provider. This setup *must* be defined in `app/core/logging.py` and initialized in `app/main.py`.

  * Logs *must* be formatted as human-readable console output in development (when `ENV=dev`).

  * Logs *must* be formatted as structured **JSON** in production (when `ENV=prod`).

## 6. Documentation Requirements

### 6.1. In-Code Docstrings

  * All public modules, classes, functions, and methods *must* have **Google-style docstrings**.

  * `ruff` *must* be configured to lint for this `pydocstyle` convention.

### 6.2. Static Documentation Site

  * A documentation site *must* be generated using `mkdocs` with the `mkdocs-material` theme.

  * The site *must* include:

      * A "Getting Started" guide (from `CONTRIBUTING.md`).

      * A "Development" guide (explaining the `justfile` and architecture).

      * An "API Reference" section.

### 6.3. Automated API Reference

  * The "API Reference" section *must* be generated automatically using `mkdocstrings`.

  * `mkdocstrings` *must* be configured to parse the Google-style docstrings from the API router files (e.g., `app/modules/user/routes.py`).

## 7. Containerization & Deployment

### 7.1. Production `Dockerfile`

  * A multi-stage `Dockerfile` *must* be created.

  * **Stage 1 (Builder):** Installs `uv`, copies `pyproject.toml`, and installs *only* production dependencies (`uv sync --no-dev`).

  * **Stage 2 (Final):** Copies the installed dependencies from the builder and the application code (`app/`).

  * The final `CMD` *must* be `["fastapi", "run", "app/main.py", "--host", "0.0.0.0", "--port", "8000"]`.

### 7.2. Local Development (`docker-compose.yml`)

  * A `docker-compose.yml` file *must* be provided to orchestrate the full local environment.

  * It *must* define two services:

    1.  `api`: The FastAPI app (built from `Dockerfile`).

    2.  `db`: The `postgres:18` image.

  * The `api` service *must* override the container's `command` to use `fastapi dev` for live-reloading.

  * The `api` service *must* use `volumes` to mount the local `app/` directory for live-reload.

## 8. Quality Assurance & CI/CD

### 8.1. Testing

  * All business logic *must* be unit-tested using `pytest`.

  * Tests *must* be written using `pytest-asyncio` for async code.

  * API endpoints *must* be integration-tested using `httpx.AsyncClient`.

### 8.2. Continuous Integration (CI)

  * A CI pipeline (e.g., GitHub Actions) *must* be configured.

  * The pipeline *must* run on every push and pull request.

  * The CI pipeline *must* execute the following:

    1.  Install all dependencies: `just install`.

    2.  Run all quality checks: `just check` (which includes format, lint, typecheck, and test).

    3.  Build the documentation: `just docs-build`.

-----

## 9. Version 0.1.0 - Core Features ✅

Version 0.1.0 is **COMPLETE** with the following features implemented:

* ✅ Core API framework with FastAPI
* ✅ User CRUD operations
* ✅ PostgreSQL database integration
* ✅ Async database sessions with SQLModel
* ✅ Alembic migrations
* ✅ Structured logging with structlog
* ✅ Exception handling
* ✅ 100% test coverage
* ✅ Docker containerization
* ✅ Complete developer tooling (`justfile`, pre-commit hooks)
* ✅ CI/CD pipeline
* ✅ Documentation site

## 10. Version 0.2.0 - Enhanced Features (Planned)

The following features are planned for Version 0.2.0:

1.  **Authentication:**
      * Implementation of OAuth 2.0 flows (not custom JWT).
      * Integration with Identity Providers (IdPs).
2.  **Background Tasks:**
      * Integration of `dramatiq` with Redis.
      * Dedicated `worker` container in Docker Compose.
3.  **Observability:**
      * Full OpenTelemetry (OTel) instrumentation (Traces, Metrics).
      * Integration with OTLP collectors.
