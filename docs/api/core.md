# Core API

Documentation for core infrastructure modules.

---

## Exceptions

Core exception classes for domain error handling.

### AppError

Base class for all application exceptions.

```python
from app.core.exceptions import AppError

class AppError(Exception):
    """Base class for application exceptions."""

    def __init__(
        self,
        message: str,
        status_code: int = 500,
        headers: dict[str, str] | None = None,
    ) -> None:
        self.message = message
        self.status_code = status_code
        self.headers = headers
```

**Usage:**

```python
raise AppError(message="Something went wrong", status_code=500)
```

### NotFoundError

Resource not found (404).

```python
raise NotFoundError(message="User not found")
```

### ConflictError

Resource conflict (409).

```python
raise ConflictError(message="Email already exists")
```

### BadRequestError

Invalid request (400).

```python
raise BadRequestError(message="Invalid request parameters")
```

### InternalServerError

Internal server error (500).

```python
raise InternalServerError(message="Something went wrong")
```

### ForbiddenError

Insufficient permissions (403).

```python
raise ForbiddenError(message="Admin access required")
```

**Note:** FastAPI + Pydantic automatically handle request validation and return 422 responses for invalid data. You don't need a custom `ValidationError` exception.

**Source:** [app/core/exceptions.py](https://github.com/balakmran/fastapi-backend/blob/main/app/core/exceptions.py)

---

## Configuration

Application settings loaded from environment variables.

### Settings Class

```python
from pydantic_settings import BaseSettings
from pydantic import computed_field
from pydantic_core import MultiHostUrl

class Settings(BaseSettings):
    # Environment
    APP_ENV: str = "dev"

    # Database
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "fastapi"
    POSTGRES_DRIVER: str = "postgresql+asyncpg"

    @computed_field
    @property
    def DATABASE_URL(self) -> MultiHostUrl:
        # Constructs database URL from components
        ...

    # Observability
    OTEL_ENABLED: bool = True
```

**Usage:**

```python
from app.core.config import settings

# Access configuration
database_url = settings.DATABASE_URL
is_production = settings.APP_ENV == "prod"
```

**Source:** [app/core/config.py](https://github.com/balakmran/fastapi-backend/blob/main/app/core/config.py)

---

## Exception Handlers

Global exception handlers for converting domain exceptions to HTTP responses.

### app_exception_handler

Converts `AppError` exceptions to JSON responses.

```python
async def app_exception_handler(
    request: Request, exc: AppError
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
        headers=exc.headers,
    )
```

### add_exception_handlers

Registers all exception handlers with the FastAPI app.

```python
def add_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AppError, app_exception_handler)
```

**Source:** [app/core/exception_handlers.py](https://github.com/balakmran/fastapi-backend/blob/main/app/core/exception_handlers.py)

---

## Middlewares

CORS and other middleware configuration.

### configure_middlewares

```python
def configure_middlewares(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
```

**Source:** [app/core/middlewares.py](https://github.com/balakmran/fastapi-backend/blob/main/app/core/middlewares.py)

---

## Logging

Structured logging configuration with Structlog.

### setup_logging

```python
def setup_logging() -> None:
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.dev.ConsoleRenderer()  # dev
        ],
    )
```

**Source:** [app/core/logging.py](https://github.com/balakmran/fastapi-backend/blob/main/app/core/logging.py)

---

## Telemetry

OpenTelemetry configuration for distributed tracing.

### setup_opentelemetry

```python
def setup_opentelemetry(app: FastAPI) -> None:
    if not settings.OTEL_ENABLED:
        return

    FastAPIInstrumentor.instrument_app(app)
    SQLAlchemyInstrumentor().instrument()
```

**Source:** [app/core/telemetry.py](https://github.com/balakmran/fastapi-backend/blob/main/app/core/telemetry.py)

---

## Metadata

Application metadata and OpenAPI parameters.

```python
from app.core.metadata import (
    APP_NAME,
    APP_VERSION,
    APP_DESCRIPTION,
    OPENAPI_PARAMETERS,
)
```

**Source:** [app/core/metadata.py](https://github.com/balakmran/fastapi-backend/blob/main/app/core/metadata.py)

---

## See Also

- [Error Handling Guide](../guides/error-handling.md) — Detailed exception patterns
- [Configuration Guide](../guides/configuration.md) — Environment setup
- [Observability Guide](../guides/observability.md) — Logging and tracing
