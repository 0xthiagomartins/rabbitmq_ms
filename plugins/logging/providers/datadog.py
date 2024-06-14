import logging
from nameko.dependency_providers import DependencyProvider
from ..settings import LoggerFilter, get_data_to_log
import os
from datadog import initialize
from datadog.handlers import DatadogHandler


class DatadogDependency(DependencyProvider):
    """Dependency Provider to send logs to Datadog"""

    def __test_provider_connection(self, logger: logging.Logger) -> None:
        try:
            logger.info("Test message sent to Datadog")
            print("Log message sent successfully.")
        except Exception as e:
            print(f"Error sending log message: {e}")

    def _configure_logger(
        self, logger: logging.Logger, api_key: str, log_level: str
    ) -> None:
        logger.setLevel(log_level)

        options = {"api_key": api_key}
        initialize(**options)

        handler = DatadogHandler()
        logger.addHandler(handler)
        logger.info("=" * 50)
        logger.info("Configuring Datadog")
        logger.info(f"api_key: {api_key}\nlog_level: {log_level}")
        logger.info("=" * 50)

        for h in logging.root.handlers:
            h.addFilter(LoggerFilter())

    def setup(self) -> None:
        """
        Function to configure the logging API related to Datadog.
        Collects Datadog settings from environment variables:
        - Datadog API Key
        - Log level to be sent.
        """
        logger = logging.getLogger()

        api_key = os.environ.get("DATADOG_API_KEY")
        log_level = os.environ.get("DATADOG_LOG_LEVEL")

        self._configure_logger(logger, api_key, log_level)
        self.__test_provider_connection(logger)

    def get_dependency(self, worker_ctx) -> logging.Logger:
        return logging.getLogger()
