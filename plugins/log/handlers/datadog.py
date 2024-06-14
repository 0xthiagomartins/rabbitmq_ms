import logging, os
from datadog import initialize
from datadog_logger import DatadogLogHandler
from ..base import LogHandlerBase
from nameko.exceptions import ConfigurationError  # type: ignore


class DatadogHandler(LogHandlerBase):
    def __create_handler(self):
        API_KEY = os.getenv("DATADOG_API_KEY")
        APP_KEY = os.getenv("DATADOG_APP_KEY")
        if not all([API_KEY, APP_KEY]):
            raise ConfigurationError(
                "Missing Datadog configuration environment variables."
            )

        options = {
            "api_key": API_KEY,
            "app_key": APP_KEY,
        }
        initialize(**options)
        handler = DatadogLogHandler()
        return handler

    def __test_handler_connection(self, logger):
        try:
            logger.info("Test message sent to Graylog")
        except Exception as e:
            print(f"Error sending log message: {e}")

    def setup(self):
        handler = self.__create_handler()
        logger = self.configure_logger()
        logger.addHandler(handler)
        self.configure_handlers()
        self.__test_handler_connection(logger)

    def get_logger(self):
        return logging.getLogger()
