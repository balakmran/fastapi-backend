# Configuration

The application is configured using **environment variables** and **[Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)**. This ensures strict type validation for all configuration options.

## Environment Variables

Configuration is loaded from a `.env` file in the project root.

### Setup

Copy the example configuration to create your local `.env` file:

```bash
cp .env.example .env
```

### Key Settings

| Variable       | Description                     | Default                                                        |
| :------------- | :------------------------------ | :------------------------------------------------------------- |
| `APP_ENV`      | App environment (`dev`, `prod`) | `dev`                                                          |
| `OTEL_ENABLED` | Enable OpenTelemetry            | `true`                                                         |
| `DATABASE_URL` | PostgreSQL connection string    | `postgresql+psycopg://postgres:postgres@localhost:5432/app_db` |

## Core Settings Module

All settings are defined in `app/core/config.py`. The `Settings` class defines the schema and validation rules.

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_ENV: str = "dev"
    OTEL_ENABLED: bool = True
    # ...
```

## Database Configuration

The database connection is managed in `app/db/session.py`. It uses `SQLModel` (a wrapper around SQLAlchemy) with the async `asyncpg` driver for high performance.

- **Changes**: Never modify the database schema manually. Always change the `SQLModel` definition in Python.
- **Migrations**: Use `just migrate-gen "message"` to generate migration scripts.
