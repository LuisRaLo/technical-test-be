import json
import os
from logging import Formatter, NullHandler, StreamHandler, getLogger
from typing import Any, Dict, Optional


class CustomLogger:
    """
    A custom logger class optimized for AWS Lambda environments.
    """

    def __init__(
        self, logger_name: Optional[str] = None, level_log: str = "INFO"
    ) -> None:
        """
        Initialize a new CustomLogger instance.
        """
        self.logger_name = logger_name or __name__
        self.level_log = level_log.upper()
        self.logger = getLogger(self.logger_name)
        self.is_lambda = "AWS_LAMBDA_FUNCTION_NAME" in os.environ
        self._setup_logger()

    def _setup_logger(self) -> None:
        """Configure the logger based on the environment."""
        # Clear any existing handlers
        if self.logger.handlers:
            self.logger.handlers.clear()

        # Set logging level
        self.logger.setLevel(self.level_log)

        if not self.is_lambda:
            # Only add StreamHandler if not in Lambda environment
            console_handler = StreamHandler()
            console_handler.setLevel(self.level_log)

            formatter = Formatter(
                fmt="%(name)s: %(asctime)s | %(levelname)s | %(filename)s:%(lineno)s | %(process)d >>> %(message)s",
                datefmt="%m/%d/%Y %I:%M:%S %p",
            )

            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
        else:
            # In Lambda, we'll just use print for the actual logging
            self.logger.addHandler(NullHandler())

    def _format_message(
        self, message: str, extra: Optional[Dict[str, Any]] = None
    ) -> str:
        """Format the message with extra parameters."""
        if extra:
            try:
                extra_str = json.dumps(extra, default=str)
                return f"{message} | {extra_str}"
            except Exception:
                return f"{message} | {str(extra)}"
        return message

    def info(self, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """Log an info message."""
        formatted_message = self._format_message(message, extra)
        if self.is_lambda:
            print(
                formatted_message
            )  # Lambda will automatically add timestamp and request ID
        else:
            self.logger.info(formatted_message)

    def error(self, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """Log an error message."""
        formatted_message = self._format_message(message, extra)
        if self.is_lambda:
            print(f"ERROR: {formatted_message}")
        else:
            self.logger.error(formatted_message)

    def debug(self, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """Log a debug message."""
        formatted_message = self._format_message(message, extra)
        if self.is_lambda:
            print(f"DEBUG: {formatted_message}")
        else:
            self.logger.debug(formatted_message)

    def warning(self, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """Log a warning message."""
        formatted_message = self._format_message(message, extra)
        if self.is_lambda:
            print(f"WARNING: {formatted_message}")
        else:
            self.logger.warning(formatted_message)

    def critical(self, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """Log a critical message."""
        formatted_message = self._format_message(message, extra)
        if self.is_lambda:
            print(f"CRITICAL: {formatted_message}")
        else:
            self.logger.critical(formatted_message)
