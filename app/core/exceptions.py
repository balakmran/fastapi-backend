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
