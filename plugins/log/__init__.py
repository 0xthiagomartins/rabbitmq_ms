import os
from nameko.extensions import DependencyProvider  # type: ignore
from nameko.exceptions import ConfigurationError  # type: ignore
from .providers import GraylogProvider, DatadogProvider


class LoggerDependencyProvider(DependencyProvider):
    def __init__(self):
        self.provider_name = os.getenv("LOG_PROVIDER", "graylog").lower()
        self.provider = None

    def setup(self):
        if self.provider_name == "graylog":
            self.provider = GraylogProvider()
        elif self.provider_name == "datadog":
            self.provider = DatadogProvider()
        else:
            raise ConfigurationError(f"Unsupported log provider: {self.provider_name}")

        self.provider.setup()

    def get_dependency(self, worker_ctx):
        return self.provider.get_logger()
