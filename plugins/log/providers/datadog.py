import logging, os
from datadog import initialize
from datadog_logger import DatadogLogHandler
from ..base import LogProviderBase, LoggerFilter
from nameko.exceptions import ConfigurationError  # type: ignore


class DatadogProvider(LogProviderBase):
    def setup(self):
        api_key = os.getenv("DATADOG_API_KEY")
        app_key = os.getenv("DATADOG_APP_KEY")

        if not all([api_key, app_key]):
            raise ConfigurationError(
                "Missing Datadog configuration environment variables."
            )

        options = {
            "api_key": api_key,
            "app_key": app_key,
        }
        initialize(**options)

        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        # Add DatadogLogHandler
        handler = DatadogLogHandler()
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        for h in logging.root.handlers:
            h.addFilter(LoggerFilter())

        self.logger = logger

    def get_logger(self):
        return self.logger
