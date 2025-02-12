import unittest
from unittest import mock
from src.infrastructure.utils.logger import (
    CustomLogger,
)


class TestCustomLogger(unittest.TestCase):
    @mock.patch("src.infrastructure.utils.logger.CustomLogger")
    def test_custom_logger(self, mock_logger_class):
        mock_logger_instance = mock.MagicMock()
        mock_logger_class.return_value = mock_logger_instance

        mock_logger_instance.info.return_value = None

        logger = CustomLogger("INFO")  # Simulamos la creación de un logger
        logger.info("This is a test log")

        mock_logger_instance.info.assert_called_with("This is a test log")
