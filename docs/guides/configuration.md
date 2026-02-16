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

| Variable            | Description                     | Default     |
| :------------------ | :------------------------------ | :---------- |
| `APP_ENV`           | App environment (`dev`, `prod`) | `dev`       |
| `OTEL_ENABLED`      | Enable OpenTelemetry            | `true`      |
| `POSTGRES_HOST`     | PostgreSQL host                 | `localhost` |
| `POSTGRES_PORT`     | PostgreSQL port                 | `5432`      |
| `POSTGRES_USER`     | PostgreSQL username             | `postgres`  |
| `POSTGRES_PASSWORD` | PostgreSQL password             | `postgres`  |
| `POSTGRES_DB`       | PostgreSQL database name        | `app_db`    |

## Core Settings Module

All settings are defined in `app/core/config.py`. The `Settings` class defines the schema and validation rules.

```python
from pydantic import PostgresDsn, computed_field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_ENV: str = "dev"
    OTEL_ENABLED: bool = True

    # Database - constructed from individual POSTGRES_* vars
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "postgres"
    # ... other POSTGRES_* fields

    @computed_field
    @property
    def DATABASE_URL(self) -> PostgresDsn:
        """Assemble the database URL."""
        # ... constructed from POSTGRES_* fields
```

## Database Configuration

The database connection is managed in `app/db/session.py`. The async
engine is created via `create_db_engine()` and stored on
`app.state.engine` during the application lifespan. It uses `SQLModel`
(a wrapper around SQLAlchemy) with the async `asyncpg` driver for high
performance.

- **Changes**: Never modify the database schema manually. Always change the `SQLModel` definition in Python.
- **Migrations**: Use `just migrate-gen "message"` to generate migration scripts.

---

## See Also

- [Database Migrations Guide](database-migrations.md) — Managing schema changes
- [.env.example](https://github.com/balakmran/fastapi-backend/blob/main/.env.example) — Environment variables template
- [app/core/config.py](https://github.com/balakmran/fastapi-backend/blob/main/app/core/config.py) — Settings module
