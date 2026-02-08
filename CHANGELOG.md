# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2025-12-08

### Added

- **Home Page**: A beautiful, dark-themed landing page with feature highlights and quick start snippet.
- **Readiness Probe**: New `/ready` endpoint to check database connectivity.
- **System Module**: dedicated `app/modules/system` for core endpoints (`/`, `/health`, `/ready`).
- **Favicon**: Official FastAPI logo served as the favicon.
- **AI Context**: Added `GEMINI.md` for AI agent instructions and project context.
- **Versioning**: Implemented dynamic versioning and automated bump workflow (`just bump`).
- **Release Automation**: Added `just tag` to automate git tagging and pushing.
- **Documentation**: Updated `CONTRIBUTING.md` and `GEMINI.md` with versioning workflow instructions.

### Changed

- **OpenAPI Metadata**: Improved title, summary, and description in `/docs` using detailed info from README.
- **Swagger UI**: Hidden "Schemas" section by default for a cleaner interface.
- **Refactoring**: Moved root and health endpoints out of `main.py` to `system` module.

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
