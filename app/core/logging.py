import logging
import sys
from collections.abc import MutableMapping
from typing import Any

import structlog
from opentelemetry import trace
from structlog.types import Processor

from app.core.config import Environment, settings


def _add_otel_context(
    logger: Any, method: str, event_dict: MutableMapping[str, Any]
) -> MutableMapping[str, Any]:
    """Inject active OTel trace_id and span_id into every log event."""
    span = trace.get_current_span()
    ctx = span.get_span_context()
    if ctx.is_valid:
        event_dict["trace_id"] = format(ctx.trace_id, "032x")
        event_dict["span_id"] = format(ctx.span_id, "016x")
    return event_dict


# The list instance handed to structlog.configure() below. setup_logging()
# runs on every create_app() call, not just once at process start, so this
# is kept as one persistent list mutated in place (clear + extend) rather
# than rebound to a fresh list each time.
#
# structlog.testing.capture_logs() works by mutating *this exact list
# object* in place (see its docstring: "keep the list instance intact to
# not break references held by bound loggers"). A module-level logger
# cached via cache_logger_on_first_use=True captures a reference to
# whatever list object was live at its first real log call; if
# setup_logging() replaced that list wholesale on a later call, the
# cached logger would keep pointing at the old, abandoned list and
# capture_logs() -- which only ever mutates the *current* list -- would
# silently stop seeing that logger's output.
_processors: list[Processor] = []


def setup_logging() -> None:
    """Configure structured logging."""
    # Processors compatible with both PrintLogger and stdlib logger
    shared_processors = [
        structlog.contextvars.merge_contextvars,
        _add_otel_context,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        # UTC in production so aggregated JSON logs are timezone-stable
        # across hosts; local time in dev/test keeps console logs
        # readable against the wall clock.
        structlog.processors.TimeStamper(
            fmt="iso", utc=settings.ENV == Environment.production
        ),
    ]

    if settings.ENV == Environment.production:
        processors = [
            # Only for prod (needs stdlib logger)
            structlog.stdlib.add_logger_name,
            *shared_processors,
            structlog.processors.dict_tracebacks,
            structlog.processors.JSONRenderer(),
        ]
    else:
        # ConsoleRenderer formats exc_info itself (prettier tracebacks).
        # Drop format_exc_info here, or it pre-renders exc_info to a
        # string and ConsoleRenderer emits a UserWarning.
        console_processors = [
            p
            for p in shared_processors
            if p is not structlog.processors.format_exc_info
        ]
        processors = [
            *console_processors,
            structlog.dev.ConsoleRenderer(
                pad_event_to=0
            ),  # No padding for compact logs
        ]

    # Mutate the persistent list in place instead of handing configure()
    # a new list -- see the comment on _processors above.
    _processors.clear()
    _processors.extend(processors)

    structlog.configure(
        processors=_processors,
        logger_factory=structlog.PrintLoggerFactory()
        if settings.ENV == Environment.development
        else structlog.stdlib.LoggerFactory(),
        # The filtering wrapper is what enforces QUOIN_LOG_LEVEL;
        # structlog.stdlib.BoundLogger has no level filter of its own.
        wrapper_class=structlog.make_filtering_bound_logger(settings.LOG_LEVEL),
        cache_logger_on_first_use=True,
    )

    # Configure standard library logging for third-party libraries
    if settings.ENV != Environment.development:
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
        root_logger.setLevel(settings.LOG_LEVEL)
