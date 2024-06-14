import os
from nameko.extensions import DependencyHandler  # type: ignore
from nameko.exceptions import ConfigurationError  # type: ignore
from .handlers import GraylogHandler, DatadogHandler, LocalHandler


class LoggerDependencyHandler(DependencyHandler):
    def __init__(self):
        self.handler_name = os.getenv("LOG_HANDLER", "local").lower()
        self.handler = None

    def setup(self):
        match self.handler_name:
            case "graylog":
                self.handler = GraylogHandler()
            case "datadog":
                self.handler = DatadogHandler()
            case "local":
                self.handler = LocalHandler()
            case _:
                raise ConfigurationError(f"Unsupported log handler: {_}")

        self.handler.setup()

    def get_dependency(self, worker_ctx):
        return self.handler.get_logger()
