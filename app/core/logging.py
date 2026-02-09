import logging
import sys

import structlog

from app.core.config import settings


def setup_logging() -> None:
    """Configure structured logging."""
    # Processors compatible with both PrintLogger and stdlib logger
    shared_processors = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.TimeStamper(fmt="iso", utc=False),
    ]

    if settings.ENV == "prod":
        processors = [
            # Only for prod (needs stdlib logger)
            structlog.stdlib.add_logger_name,
            *shared_processors,
            structlog.processors.dict_tracebacks,
            structlog.processors.JSONRenderer(),
        ]
    else:
        processors = [
            *shared_processors,
            structlog.dev.ConsoleRenderer(
                pad_event_to=0
            ),  # No padding for compact logs
        ]

    structlog.configure(
        processors=processors,
        logger_factory=structlog.PrintLoggerFactory()
        if settings.ENV == "dev"
        else structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    # Configure standard library logging for third-party libraries
    if settings.ENV != "dev":
        # Only needed in production when we use LoggerFactory
        formatter = structlog.stdlib.ProcessorFormatter(
            foreign_pre_chain=shared_processors,
            processors=[
                structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                structlog.processors.JSONRenderer(),
            ],
        )

        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(formatter)

        root_logger = logging.getLogger()
        root_logger.handlers.clear()
        root_logger.addHandler(handler)
        root_logger.setLevel(logging.INFO)
