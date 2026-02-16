from __future__ import annotations


class AppError(Exception):
    """Base class for application exceptions."""

    def __init__(
        self,
        message: str,
        status_code: int = 500,
        headers: dict[str, str] | None = None,
    ) -> None:
        """Initialize AppError."""
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.headers = headers


class InternalServerError(AppError):
    """Internal Server Error."""

    def __init__(
        self,
        message: str = "Internal Server Error",
        headers: dict[str, str] | None = None,
    ) -> None:
        """Initialize InternalServerError."""
        super().__init__(message, status_code=500, headers=headers)


class NotFoundError(AppError):
    """Resource Not Found."""

    def __init__(
        self,
        message: str = "Not Found",
        headers: dict[str, str] | None = None,
    ) -> None:
        """Initialize NotFoundError."""
        super().__init__(message, status_code=404, headers=headers)


class ConflictError(AppError):
    """Resource Conflict."""

    def __init__(
        self,
        message: str = "Conflict",
        headers: dict[str, str] | None = None,
    ) -> None:
        """Initialize ConflictError."""
        super().__init__(message, status_code=409, headers=headers)


class BadRequestError(AppError):
    """Bad Request."""

    def __init__(
        self,
        message: str = "Bad Request",
        headers: dict[str, str] | None = None,
    ) -> None:
        """Initialize BadRequestError."""
        super().__init__(message, status_code=400, headers=headers)


class ForbiddenError(AppError):
    """Forbidden."""

    def __init__(
        self,
        message: str = "Forbidden",
        headers: dict[str, str] | None = None,
    ) -> None:
        """Initialize ForbiddenError."""
        super().__init__(message, status_code=403, headers=headers)


__all__ = [
    "AppError",
    "BadRequestError",
    "ConflictError",
    "ForbiddenError",
    "InternalServerError",
    "NotFoundError",
]
