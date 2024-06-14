import os
from nameko.extensions import DependencyProvider  # type: ignore
from nameko.exceptions import ConfigurationError  # type: ignore
from .providers import GraylogProvider, DatadogProvider, LocalProvider


class LoggerDependencyProvider(DependencyProvider):
    def __init__(self):
        self.provider_name = os.getenv("LOG_PROVIDER", "local").lower()
        self.provider = None

    def setup(self):
        match self.provider_name:
            case "graylog":
                self.provider = GraylogProvider()
            case "datadog":
                self.provider = DatadogProvider()
            case "local":
                self.provider = LocalProvider()
            case _:
                raise ConfigurationError(f"Unsupported log provider: {_}")

        self.provider.setup()

    def get_dependency(self, worker_ctx):
        return self.provider.get_logger()
