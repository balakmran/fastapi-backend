# FastAPI Backend

[![CI](https://github.com/balakmran/fastapi-backend/actions/workflows/ci.yml/badge.svg)](https://github.com/balakmran/fastapi-backend/actions/workflows/ci.yml)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-261230.svg)](https://github.com/astral-sh/ruff)

**High-Performance, Scalable API Foundation** built with **FastAPI**,
**SQLModel**, and **PostgreSQL**. Features a production-ready stack with strict
type checking, structured logging, and OpenTelemetry observability.

## 🚀 Key Features

- **High Performance**: Async I/O with FastAPI and Pydantic.
- **Type Safe**: 100% type-annotated, verified by `ty`.
- **Observable**: integrated OpenTelemetry traces and structured logging.
- **Developer First**: Powered by `uv` for package management and `just` for
  automation.

## 🛠️ Tech Stack

- **Core**: FastAPI, SQLModel, Pydantic Settings
- **Database**: PostgreSQL, AsyncPG, Alembic
- **Tooling**: uv, Ruff, Ty, Pytest
- **Observability**: OpenTelemetry, Structlog

## ⚡️ Quick Start

```bash
# 1. Setup project (install dependencies & pre-commit hooks)
just setup

# 2. Start database (Docker)
just db

# 3. Run migrations
just migrate-up

# 4. Start server
just run
```

Visit the API documentation at
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## 📂 Project Structure

```plaintext
├── app/
│   ├── core/
│   │   ├── config.py             # Pydantic settings
│   │   ├── exceptions.py         # Custom exceptions
│   │   ├── exception_handlers.py # Global exception handlers
│   │   ├── logging.py            # Structlog configuration
│   │   ├── metadata.py           # Application metadata
│   │   ├── middlewares.py        # Middleware configuration
│   │   ├── openapi.py            # OpenAPI metadata & config
│   │   └── telemetry.py          # OpenTelemetry instrumentation
│   ├── db/                       # Database connection & base models
│   ├── modules/
│   │   └── user/                 # Example domain module
│   │       ├── models.py         # SQLModel database tables
│   │       ├── schemas.py        # Pydantic request/response models
│   │       ├── repository.py     # Database access (CRUD)
│   │       ├── service.py        # Business logic
│   │       └── routes.py         # FastAPI router endpoints
│   ├── static/                   # Static assets (css, img)
│   ├── templates/                # Jinja2 templates
│   └── main.py                   # App entry point
├── tests/                        # Pytest suite
├── alembic/                      # Database migrations
├── docs/                         # Documentation
├── .env.example                # Environment variables template
├── docker-compose.yml            # Local dev environment
├── Dockerfile                    # Production Docker image
├── GEMINI.md                     # AI Agent context
├── justfile                      # Command runner
├── pyproject.toml                # Dependencies & config
└── zensical.toml                 # Documentation config
```

## 📚 Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

## 📜 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute to this
project.

## License

This project is licensed under the terms of the [MIT license](LICENSE).
