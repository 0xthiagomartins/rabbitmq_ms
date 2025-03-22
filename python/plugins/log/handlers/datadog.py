import os
from datadog import initialize
from datadog_logger import DatadogLogHandler
from nameko.exceptions import ConfigurationError  # type: ignore


class DatadogHandler:
    def __init__(self):
        handler = self.__create_handler()
        return handler

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
