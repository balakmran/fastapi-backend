# FastAPI Backend - Project Context

## Project Overview

This is a robust backend API built with **FastAPI**, **SQLModel**, and **PostgreSQL**. It is designed as a scalable foundation for high-performance web applications, featuring a modern Python stack (Python 3.12+) and developer-focused tooling (`uv`, `just`, `ruff`).

## 🛠 Tech Stack & Tools

- **Framework:** FastAPI
- **Database:** PostgreSQL (using `asyncpg` driver)
- **ORM:** SQLModel (SQLAlchemy wrapper)
- **Migrations:** Alembic
- **Package Manager:** `uv` (Fast Python package installer)
- **Task Runner:** `just`
- **Linting/Formatting:** Ruff
- **Type Checking:** ty (Static type checker)
- **Testing:** Pytest, pytest-cov

## 🚀 Key Commands (via `just`)

The project uses `just` to automate common tasks.

| Command                    | Action                                                      |
| :------------------------- | :---------------------------------------------------------- |
| `just install`             | Install all dependencies (dev included) using `uv`.         |
| `just run`                 | Start the local development server (auto-reload enabled).   |
| `just up`                  | Start all services (App + DB) via Docker Compose.           |
| `just db`                  | Start only the PostgreSQL database container.               |
| `just down`                | Stop and remove all Docker containers.                      |
| `just check`               | Run **all** quality checks (format, lint, typecheck, test). |
| `just test`                | Run tests with coverage reporting.                          |
| `just migrate-gen "<msg>"` | Generate a new Alembic migration.                           |
| `just migrate-up`          | Apply pending database migrations.                          |
| `just clean`               | Remove build artifacts and cache.                           |

## 📂 Architecture

The project follows a modular structure within the `app/` directory:

- **`app/main.py`**: Application entry point. Configures lifecycle, middleware, and exception handlers.
- **`app/core/`**: Core infrastructure.
  - `config.py`: Application settings using `pydantic-settings` (reads `.env`).
  - `logging.py`: Structured logging setup (structlog).
  - `exceptions.py`, `exception_handlers.py`: Global error handling.
- **`app/db/`**: Database configuration (`session.py`, `base.py`).
- **`app/modules/`**: Feature modules (Domain-Driven Design).
  - Example: `app/modules/user/` contains `models.py`, `schemas.py`, `routes.py`, `service.py`, `repository.py`.
- **`tests/`**: Test suite mirroring the app structure.
- **`alembic/`**: Database migration scripts.

## 📝 Development Conventions

### Code Quality

- **Formatting & Linting:** Strictly enforced by **Ruff**.
- **Type Safety:** 100% type hint coverage expected. Checked by `ty`.
- **Docstrings:** Google-style docstrings are used (configured in `pyproject.toml`).

### Coding Standards

- **Python:** Adhere to the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html).
- **General:** For other languages or aspects, refer to the [Google Style Guides](https://google.github.io/styleguide/) for consistent coding standards across the project.

### Database Changes

- **Never modify the database schema manually.**
- Always define models in code (SQLModel) and run `just migrate-gen "message"` to generate a migration script.
- Apply changes with `just migrate-up`.

### Configuration

- Environment variables are managed via `.env` files.
- Configuration is loaded into the `Settings` class in `app/core/config.py`.
- `uv.lock` ensures deterministic dependency resolution.

### Testing

- Tests are written using `pytest`.
- Run `just test` to execute the suite.
- Ensure high test coverage for new features.

## 🔑 Key Files

- `justfile`: Definition of all executable task commands.
- `pyproject.toml`: Project configuration, dependencies, and tool settings (Ruff, Pytest).
- `docker-compose.yml`: Definition of local dev services (Postgres).
- `app/main.py`: The FastAPI application factory.

### 🧩 Feature Module Template

When creating a new module (e.g., `app/modules/product/`), follow this structure:

- `models.py`: SQLModel database tables.
- `schemas.py`: Pydantic models for Request/Response (keep separate from DB models).
- `repository.py`: CRUD operations (database interaction only).
- `service.py`: Business logic (calls repository).
- `routes.py`: FastAPI router endpoints (calls service).
- `__init__.py`: Expose the router as `router`.

### 🧪 Testing Guidelines

- **Fixtures:** Use `conftest.py` for shared resources (db session, async client).
- **Integration over Unit:** Prioritize integration tests for routes (`tests/modules/user/test_routes.py`).
- **Mocking:** Mock external APIs, but use a real (test) database for repository tests.
- **Naming:** Test functions must start with `test_` and be descriptive (e.g., `test_create_user_duplicate_email_fails`).

### 📦 Git & Commits

- **Conventional Commits:** Use the format `<type>(<scope>): <description>`.
  - Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`.
  - Example: `feat(user): add password reset endpoint`

### ⚠️ Error Handling

- Use the custom `AppException` (or specific subclasses) for logic errors.
- **Do not** raise generic HTTPExceptions (`HTTPException(status_code=400)`) in services; raise domain exceptions instead, and let the router or exception handler map them to HTTP status codes.

### 🚀 Release Process

- **Versioning:** Use Semantic Versioning (Major.Minor.Patch).
- **Automation:** Use `just bump part="<part>"` to increment the version. This updates `pyproject.toml` and `app/__init__.py`.

  | Run Command              | Bump Type | Result (Original: 0.2.0) |
  | :----------------------- | :-------- | :----------------------- |
  | `just bump part="patch"` | Patch     | `0.2.1`                  |
  | `just bump part="minor"` | Minor     | `0.3.0`                  |
  | `just bump part="major"` | Major     | `1.0.0`                  |

- **Changelog:** Always update `CHANGELOG.md` with a new version header and release date before bumping the version.
