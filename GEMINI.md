# AI Agent Instructions

## Project Overview

**High-Performance, Scalable API Foundation** built with **FastAPI**,
**SQLModel**, and **PostgreSQL**. Features a production-ready stack with strict
type checking, structured logging, and OpenTelemetry observability.

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
- **Observability:** OpenTelemetry, Structlog
- **Documentation:** Zensical (MkDocs Material)

## 🚀 Key Commands (via `just`)

The project uses `just` to automate common tasks.

| Command                    | Action                                                      |
| :------------------------- | :---------------------------------------------------------- |
| `just setup`               | Setup project (install dependencies and pre-commit hooks).  |
| `just install`             | Install all dependencies (dev included) using `uv`.         |
| `just run`                 | Start the local development server (auto-reload enabled).   |
| `just up`                  | Start all services (App + DB) via Docker Compose.           |
| `just db`                  | Start only the PostgreSQL database container.               |
| `just down`                | Stop and remove all Docker containers.                      |
| `just check`               | Run **all** quality checks (format, lint, typecheck, test). |
| `just format`              | Auto-format code with Ruff.                                 |
| `just lint`                | Check code quality with Ruff.                               |
| `just typecheck`           | Verify type annotations with ty.                            |
| `just test`                | Run test suite with coverage.                               |
| `just clean`               | Remove build artifacts and cache.                           |
| `just pi`                  | Install pre-commit hooks.                                   |
| `just pr`                  | Run pre-commit hooks on all files.                          |
| `just docb`                | Build documentation.                                        |
| `just ds`                  | Serve documentation locally.                                |
| `just migrate-gen "<msg>"` | Generate a new Alembic migration.                           |
| `just migrate-up`          | Apply pending database migrations.                          |
| `just migrate-down`        | Rollback last migration.                                    |
| `just bump part="<type>"`  | Bump version (patch, minor, major).                         |
| `just tag`                 | Create and push git tag for release.                        |

## 📂 Architecture

The project follows a modular structure within the `app/` directory:

- **`app/main.py`**: Application entry point. Configures lifecycle, middleware,
  and exception handlers.
- **`app/core/`**: Core infrastructure.
  - `config.py`: Application settings using `pydantic-settings` (reads `.env`).
  - `logging.py`: Structured logging setup (structlog).
  - `metadata.py`: Application metadata (version, description, URLs).
  - `openapi.py`: OpenAPI/Swagger configuration.
  - `telemetry.py`: OpenTelemetry instrumentation.
  - `middlewares.py`: Middleware configuration.
  - `exceptions.py`, `exception_handlers.py`: Global error handling.
- **`app/db/`**: Database configuration. Engine stored on `app.state.engine`.
- **`app/modules/`**: Feature modules (Domain-Driven Design).
  - Example: `app/modules/user/` contains `models.py`, `schemas.py`,
    `routes.py`, `service.py`, `repository.py`.
  - `system/`: Health checks and system status endpoints.
- **`tests/`**: Test suite mirroring the app structure.
- **`alembic/`**: Database migration scripts.
- **`docs/`**: Zensical-powered documentation site.
- **`scripts/`**: Utility scripts (e.g., docs sync).

## 📝 Development Conventions

### Code Quality

- **Formatting & Linting:** Strictly enforced by **Ruff**.
- **Type Safety:** 100% type hint coverage expected. Checked by `ty`.
- **Docstrings:** Google-style docstrings are used (configured in
  `pyproject.toml`).
- **Line Length:** Maximum 80 characters for both Code (Python) and
  Documentation (Markdown). **Exception:** Tables and code blocks are exempt.
- **Quality Checks:** Run `just check` before committing. All checks must pass.

### Coding Standards

- **Python:** Adhere to the
  [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html).
- **General:** For other languages or aspects, refer to the
  [Google Style Guides](https://google.github.io/styleguide/) for consistent
  coding standards across the project.

### Database Changes

- **Never modify the database schema manually.**
- Always define models in code (SQLModel) and run `just migrate-gen "message"`
  to generate a migration script.
- Review the generated migration before applying.
- Apply changes with `just migrate-up`.
- Rollback if needed with `just migrate-down`.

### Configuration

- Environment variables are managed via `.env` files.
- Copy `.env.example` to `.env` for local development.
- Configuration is loaded into the `Settings` class in `app/core/config.py`.
- `uv.lock` ensures deterministic dependency resolution.

### Testing

- Tests are written using `pytest`.
- Run `just test` to execute the suite with coverage.
- Run `just check` to run all quality checks (includes tests).
- Ensure ≥95% test coverage for new features.
- **Philosophy**: Integration tests over unit tests. Use real database.

## 🔑 Key Files

- `justfile`: Definition of all executable task commands.
- `pyproject.toml`: Project configuration, dependencies, and tool settings
  (Ruff, Pytest).
- `docker-compose.yml`: Definition of local dev services (Postgres).
- `Dockerfile`: Production-ready container image.
- `app/main.py`: The FastAPI application factory.
- `zensical.toml`: Documentation site configuration.

### 🧩 Feature Module Template

When creating a new module (e.g., `app/modules/product/`), follow this
structure:

- `models.py`: SQLModel database tables.
- `schemas.py`: Pydantic models for Request/Response (keep separate from DB
  models).
- `repository.py`: CRUD operations (database interaction only).
- `service.py`: Business logic (calls repository).
- `routes.py`: FastAPI router endpoints (calls service).
- `__init__.py`: Expose the router as `router`.

**Example workflow**:

1. Create models in `models.py`
2. Generate migration: `just migrate-gen "add product model"`
3. Create schemas in `schemas.py`
4. Implement repository in `repository.py`
5. Implement service in `service.py`
6. Create routes in `routes.py`
7. Register router in `app/api.py`
8. Write tests in `tests/modules/product/`

### 🧪 Testing Guidelines

- **Fixtures:** Use `conftest.py` for shared resources (db session, async
  client).
- **Integration over Unit:** Prioritize integration tests for routes
  (`tests/modules/user/test_routes.py`).
- **Mocking:** Mock external APIs, but use a real (test) database for repository
  tests.
- **Naming:** Test functions must start with `test_` and be descriptive (e.g.,
  `test_create_user_duplicate_email_fails`).
- **Coverage:** Maintain ≥95% coverage. View reports with
  `pytest --cov=app --cov-report=html`.

### 📦 Git & Commits

- **Conventional Commits:** Use the format `<type>(<scope>): <description>`.
  - Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`.
  - Example: `feat(user): add password reset endpoint`
- **Pre-commit Hooks:** Install with `just pi`, run manually with `just pr`.
- **Branches:** Feature branches from `main`, merge via PR.

### ⚠️ Error Handling

- Use the custom `AppError` (or specific subclasses) for logic errors.
- **Do not** raise generic HTTPExceptions (`HTTPException(status_code=400)`) in
  services; raise domain exceptions instead, and let the router or exception
  handler map them to HTTP status codes.
- **Available exceptions**: `NotFoundError`, `ConflictError`, `BadRequestError`,
  `ForbiddenError`, `InternalServerError`.
- **Example**:

  ```python
  from app.core.exceptions import ConflictError

  if existing_user:
      raise ConflictError(message="Email already registered")
  ```

### 🚀 Release Process

- **Versioning:** Use Semantic Versioning (Major.Minor.Patch).
- **Workflow:**
  1. Update `CHANGELOG.md` [Unreleased] section
  2. Run `just bump part="<type>"` (patch/minor/major)
  3. Update `CHANGELOG.md` - move [Unreleased] to new version
  4. Commit changelog: `git commit -m "docs: update changelog for vX.Y.Z"`
  5. Merge to `main`
  6. Run `just tag` to create and push git tag
  7. GitHub Actions automatically creates release

  | Run Command              | Bump Type | Result (Original: 0.2.0) |
  | :----------------------- | :-------- | :----------------------- |
  | `just bump part="patch"` | Patch     | `0.2.1`                  |
  | `just bump part="minor"` | Minor     | `0.3.0`                  |
  | `just bump part="major"` | Major     | `1.0.0`                  |

- **Changelog:**
  - **Update Policy**: `CHANGELOG.md` MUST be updated after **every** meaningful
    code change.
  - **Section Order**: Within a release, group changes in the following strict
    order:
    1. `### Added` (for new features)
    2. `### Changed` (for changes in existing functionality)
    3. `### Deprecated` (for soon-to-be removed features)
    4. `### Removed` (for now removed features)
    5. `### Fixed` (for any bug fixes)
    6. `### Security` (in case of vulnerabilities)
  - Always update the `[Unreleased]` section until a new version is bumped.

### 📚 Documentation

- **Source:** All docs in `docs/` directory
- **Build:** Run `just docb` to build docs
- **Serve:** Run `just ds` to serve locally at `http://localhost:8001`
- **Sync:** Project files (CONTRIBUTING.md, CHANGELOG.md, LICENSE) are
  automatically synced to `docs/project/` during build
- **Navigation:** Configured in `zensical.toml`

**Guide Structure**:

1. Getting Started
2. Configuration
3. Database Migrations
4. Error Handling
5. Testing
6. Quality Checks (NEW)
7. Observability
8. Deployment
9. Release Workflow
10. Troubleshooting
