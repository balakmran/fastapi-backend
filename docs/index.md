# Welcome to FastAPI Backend

A robust backend API built with **FastAPI** and modern Python tooling. This project serves as a scalable foundation for building high-performance web applications.

## 🚀 Key Features

- **High Performance**: Built on [FastAPI](https://fastapi.tiangolo.com/), one of the fastest Python frameworks available.
- **Modern Stack**: Utilizes Python 3.12+, SQLModel, and Pydantic for type-safe, intuitive development.
- **Robust Design**: Includes structured logging, Docker containerization, and comprehensive configuration management.
- **Developer Experience**: Optimized workflow with `uv` for fast package management and `just` for command automation.

## 🛠️ Technology Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL with SQLModel (SQLAlchemy)
- **Migrations**: Alembic
- **Logging**: Structlog
- **Containerization**: Docker (OrbStack recommended)
- **Tooling**: uv, Ruff, ty, Pytest

## 📚 Documentation Sections

- **[Getting Started](contributing.md)**: Setup guide for new developers.
- **[Design](design/prd.md)**: Project Requirements Document (PRD).

## ⚡️ Quick Start

```bash
# Install dependencies
just install

# Start database
just db

# Run server
just run
```
