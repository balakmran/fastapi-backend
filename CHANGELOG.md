# Changelog

## [Unreleased]

### Added

- **API Versioning**: Introduced `/api/v1/` prefix to all endpoints for future-proof API evolution.
- **Module-Level Exceptions**: Added `app/modules/user/exceptions.py` and `SystemError` (in system module) for domain-specific error handling.
- **Environment Configuration**: Added `Environment` enum and `.env.test`/`.env.production` support.
- **Project Rename**: Officially renamed project from "FastAPI Backend" to **QuoinAPI** (pronounced "koyn").
- **Architectural Branding**: Updated README and Metadata with "Structural Integrity", "High-Performance Core", and "Built-in Observability" pillars.

### Changed

- **Configuration**:
  - Renamed environment variable prefix from `APP_` to `QUOIN_` (e.g., `QUOIN_ENV`, `QUOIN_DB_URL`).
  - Enforced `QUOIN_ENV` (or fallback `ENV`) to select configuration files.
  - Replaced `DEBUG` boolean with `LOG_LEVEL` string (default: "INFO").
- **Error Handling**:
  - Renamed `AppError` to `QuoinError` as the base exception class.
  - Standardized error responses with `QuoinRequestValidationError` for Pydantic errors.
  - Updated `exception_handlers.py` to use new exception hierarchy.
- **Docker**:
  - Renamed services and images to `quoin-api` and `quoin-api-docs`.
  - Updated `docker-compose.yml` to use `QUOIN_ENV` and `QUOIN_POSTGRES_*` variables.
- **Documentation**:
  - Updated all guides to reflect `QuoinAPI` naming and `QUOIN_` configuration prefix.
  - Updated branding assets and repository URLs to `balakmran/quoin-api`.

### Removed

- **Legacy Config**: Removed support for `APP_ENV` (use `QUOIN_ENV`).
- **Legacy Naming**: Removed references to `fastapi-backend` in all documentation and config files.

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
