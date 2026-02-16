from app import __version__

APP_NAME = "QuoinAPI"
APP_DESCRIPTION = (
    "The architectural cornerstone for high-performance, "
    "scalable Python services."
)
REPOSITORY_URL = "https://github.com/balakmran/quoin-api"
COPYRIGHT_OWNER = "Balakumaran Manoharan"

APP_LONG_DESCRIPTION = """
QuoinAPI (pronounced "koyn") is a high-performance, scalable foundation
designed to serve as the structural cornerstone for modern Python backends.
Built with FastAPI, SQLModel, and the Astral stack (uv, ruff, ty), it
provides a battle-tested "Golden Path" for developers who prioritize
architectural integrity, type safety, and observability.

**Key Highlights**:
- **Structural Integrity**: 100% type-annotated code verified by ty
  and strict linting via ruff
- **High-Performance Core**: Built on the speed of uv for dependency
  management and async-first patterns
- **Built-in Observability**: Integrated OpenTelemetry and structured
  logging (Structlog)
- **Architectural Efficiency**: A ready-to-use template that eliminates
  boilerplate
"""

VERSION = __version__

__all__ = [
    "APP_DESCRIPTION",
    "APP_LONG_DESCRIPTION",
    "APP_NAME",
    "COPYRIGHT_OWNER",
    "REPOSITORY_URL",
    "VERSION",
]
