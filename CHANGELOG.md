# Changelog

## [0.4.0] - 2026-02-16

### Added

- **Domain Exceptions**: `NotFoundError`, `ConflictError`, `BadRequestError`,
  `ForbiddenError` subclasses for better error handling granularity.
- **`__all__` Exports**: Explicit public API exports in all core modules and
  domain routers.
- **Pagination Guards**: `Query(ge=0)`, `Query(ge=1, le=100)` constraints on
  pagination parameters to prevent abuse.
- **Alembic in Docker**: Copied `alembic/` directory and `alembic.ini` into
  Docker image for production database migrations.

### Changed

- **Database Engine**: Refactored from global mutable engine to
  `app.state.engine` pattern for better test isolation and cleaner
  architecture.
- **Logging**: Moved `setup_logging()` call inside `create_app()` to prevent
  import-time side effects.
- **Schema Validation**: Added `extra="forbid"` to `UserBase` and `UserUpdate`
  schemas to reject extraneous fields.
- **Static Files**: Updated to use absolute paths for static files and
  templates, avoiding relative path fragility.
- **OTEL Service Name**: Now uses `metadata.APP_NAME` instead of hardcoded
  string.
- **Docker Compose**: Renamed `ENV` → `APP_ENV`, replaced stale `DATABASE_URL`
  with individual `POSTGRES_*` variables.
- **Test Fixtures**: Refactored to use `monkeypatch` for settings mutation in
  tests, avoiding direct global state modification.
- **CI Workflows**: Standardized `setup-uv` action version to `v7` across all
  workflows.
- **Documentation**: Updated Zensical config with instant navigation, prefetch,
  progress, and modern `mkdocstrings` TOML format.

### Fixed

- **`updated_at` Auto-update**: Added `onupdate` parameter to `User.updated_at`
  field to ensure automatic timestamp updates on mutations.
- **Timezone-aware Datetimes**: Fixed `datetime.now()` in `system/routes.py` to
  use `datetime.now(UTC)`.
- **Duplicate Email Status**: Changed HTTP status from `400` to `409` for
  duplicate email registration errors.
- **Alembic Offline Mode**: Fixed driver mismatch by using `postgresql+psycopg`
  instead of `postgresql+asyncpg` for offline SQL generation.
- **Exception Handler Logging**: Added structured logging for `AppError`
  exceptions in exception handlers.
- **Type Hints**: Added missing return type hints to `telemetry.py` functions.
- **Metadata References**: Fixed GEMINI.md and configuration.md to reference
  `metadata.py`, `app.state.engine`, and correct `AppError` class name.

## [0.3.1] - 2026-02-14

### Added

- **Justfile**: Added `setup` recipe to improved developer onboarding (`just setup`).

### Changed

- **Database**: Fixed `sessionmaker` usage in `app/db/session.py` to use `async_sessionmaker` for correct async support.
- **Documentation**: Updated installation guides to recommend `just setup`.
- **Prek**: Optimized `prek.toml` to use faster builtin hooks instead of GitHub pre-commit hooks.
- **Refactoring**: Extracted application metadata (version, description, URLs) to `app/core/metadata.py`.
- **Templates**: Injected dynamic metadata into `index.html` (title, description, version, copyright).
- **Swagger UI**: Hidden root endpoint (`GET /`) from API documentation.

## [0.3.0] - 2026-02-09

### Added

- **OpenTelemetry**: Integrated OpenTelemetry for production-grade distributed
  tracing and observability.
- **Zensical**: Migrated documentation engine to Zensical for a modern,
  high-performance static site.
- **Prek**: `prek` for faster hook management.

### Changed

- **Documentation**: Flattened navigation structure, added copyright footer, and
  improved Home page styling.
- **Code Quality**: Enforced stricter linting rules (80-char line limit) via
  `ruff`.

### Removed

- **Documentation**: Removed MkDocs documentation engine.
- **Pre-commit**: Removed pre-commit.

## [0.2.0] - 2025-12-08

### Added

- **Home Page**: A beautiful, dark-themed landing page with feature highlights
  and quick start snippet.
- **Readiness Probe**: New `/ready` endpoint to check database connectivity.
- **System Module**: dedicated `app/modules/system` for core endpoints (`/`,
  `/health`, `/ready`).
- **Favicon**: Official FastAPI logo served as the favicon.
- **AI Context**: Added `GEMINI.md` for AI agent instructions and project
  context.
- **Versioning**: Implemented dynamic versioning and automated bump workflow
  (`just bump`).
- **Release Automation**: Added `just tag` to automate git tagging and pushing.
- **Documentation**: Updated `CONTRIBUTING.md` and `GEMINI.md` with versioning
  workflow instructions.

### Changed

- **OpenAPI Metadata**: Improved title, summary, and description in `/docs`
  using detailed info from README.
- **Swagger UI**: Hidden "Schemas" section by default for a cleaner interface.
- **Refactoring**: Moved root and health endpoints out of `main.py` to `system`
  module.

## [0.1.0] - 2025-11-26

### Added

- Initial project setup with FastAPI, SQLModel, and PostgreSQL.
- User module with full CRUD operations (Create, Read, Update, Delete).
- Database migrations using Alembic.
- Structured logging with `structlog`.
- Docker and Docker Compose configuration for development.
- `justfile` for command automation.
- Comprehensive test suite setup with `pytest`.
- Static analysis with `ruff` and `ty`.
- Documentation with MkDocs.
