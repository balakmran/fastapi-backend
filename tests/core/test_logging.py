import logging
from unittest.mock import MagicMock, patch

import structlog

from app.core.logging import setup_logging


def test_setup_logging() -> None:
    """Test setup_logging configuration."""
    with patch("structlog.configure") as mock_configure:
        setup_logging()

        # Verify structlog.configure was called
        mock_configure.assert_called_once()

        # Verify basic logging config
        # We can check if basicConfig was called or if the handler is set
        # But since setup_logging modifies global state, we should be careful.
        # The function sets logging.basicConfig.

        # Let's verify that we can get a logger and it works
        logger = structlog.get_logger()
        assert logger is not None


def test_setup_logging_prod() -> None:
    """Test setup_logging configuration in production."""
    with (
        patch("app.core.logging.settings.ENV", "prod"),
        patch("structlog.configure") as mock_configure,
    ):
        setup_logging()

        mock_configure.assert_called_once()
        # Verify JSONRenderer is in processors
        call_args = mock_configure.call_args
        processors = call_args.kwargs["processors"]
        assert any(isinstance(p, structlog.processors.JSONRenderer) for p in processors)


def test_setup_logging_not_dev() -> None:
    """Test setup_logging stdlib configuration in non-dev environment."""
    with (
        patch("app.core.logging.settings.ENV", "prod"),
        patch("logging.getLogger") as mock_get_logger,
        patch("logging.StreamHandler"),
    ):
        mock_root_logger = MagicMock()
        mock_get_logger.return_value = mock_root_logger

        setup_logging()

        # Verify root logger handlers were cleared and new handler added
        mock_root_logger.handlers.clear.assert_called_once()
        mock_root_logger.addHandler.assert_called_once()
        mock_root_logger.setLevel.assert_called_with(logging.INFO)
