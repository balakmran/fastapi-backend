# API Reference

This section provides detailed API documentation for the FastAPI Backend,
automatically generated from the source code.

---

## Overview

The API is organized into the following modules:

### Core Modules

The [`app/core/`](core.md) package contains core infrastructure:

- **[Exceptions](core.md#exceptions)** — Domain exception classes
- **[Configuration](core.md#configuration)** — Application settings
- **[Exception Handlers](core.md#exception-handlers)** — Global error handling
- **[Middlewares](core.md#middlewares)** — CORS and other middleware
- **[Logging](core.md#logging)** — Structured logging setup
- **[Telemetry](core.md#telemetry)** — OpenTelemetry configuration
- **[Metadata](core.md#metadata)** — Application version and info

### Feature Modules

#### User Module

The [`app/modules/user/`](user.md) package provides user management:

- **[Models](user.md#models)** — Database tables (SQLModel)
- **[Schemas](user.md#schemas)** — Request/Response models (Pydantic)
- **[Repository](user.md#repository)** — Database operations (CRUD)
- **[Service](user.md#service)** — Business logic
- **[Routes](user.md#routes)** — FastAPI endpoints

---

## REST API Endpoints

### Base URL

```
http://localhost:8000/api/v1
```

### Authentication

> [!NOTE]
> Authentication is not yet implemented. All endpoints are currently
> public.

---

## Swagger Documentation

Interactive API documentation is available when running the application:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **OpenAPI JSON**: [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json)

---

## Module Index

| Module                     | Description          | Documentation                     |
| :------------------------- | :------------------- | :-------------------------------- |
| `app.core.exceptions`      | Domain exceptions    | [Core API](core.md#exceptions)    |
| `app.core.config`          | Application settings | [Core API](core.md#configuration) |
| `app.modules.user.models`  | User database model  | [User API](user.md#models)        |
| `app.modules.user.schemas` | User API schemas     | [User API](user.md#schemas)       |
| `app.modules.user.service` | User business logic  | [User API](user.md#service)       |
| `app.modules.user.routes`  | User endpoints       | [User API](user.md#routes)        |

---

## Usage Examples

### Creating a User

```python
import httpx

async with httpx.AsyncClient() as client:
    response = await client.post(
        "http://localhost:8000/api/v1/users/",
        json={
            "email": "user@example.com",
            "full_name": "John Doe"
        }
    )
    user = response.json()
    print(user)
```

### Listing Users

```python
async with httpx.AsyncClient() as client:
    response = await client.get("http://localhost:8000/api/v1/users/")
    users = response.json()
```

---

## See Also

- [System Architecture](../architecture/overview.md) — How the components fit together
- [Error Handling Guide](../guides/error-handling.md) — Exception handling patterns
- [Testing Guide](../guides/testing.md) — How to test the API
