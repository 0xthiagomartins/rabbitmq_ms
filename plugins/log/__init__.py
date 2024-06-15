import logging, os
from nameko.dependency_providers import DependencyProvider  # type: ignore
from nameko.exceptions import ConfigurationError  # type: ignore
from .handlers import GraylogHandler, DatadogHandler


class LoggerFilter(logging.Filter):
    DISCARD_FILES_OTHER_LIB = ["kombu", "pika", "werkzeug"]
    DISCARD_LEVELS_OTHER_LIB = [logging.INFO, logging.DEBUG]

    def filter(self, record: logging.LogRecord) -> int:
        try:
            for each in self.DISCARD_FILES_OTHER_LIB:
                if (
                    each in record.pathname
                    and record.levelno in self.DISCARD_LEVELS_OTHER_LIB
                ):
                    return 0

        except Exception as err:
            record.filter_exception = f"[{str(err)}] - [{str(type(err))}]"
        return 1


class LoggerDependency(DependencyProvider):
    def __init__(self):
        self.handler_name = os.getenv("LOG_HANDLER", "").lower()
        self.handler = None

    def __configure_logger(self):
        logger = logging.getLogger()
        LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
        if not all([LOG_LEVEL]):
            raise ConfigurationError(
                "Missing Basic Log configuration environment variables."
            )
        logger.setLevel(LOG_LEVEL)

        return logger

    def __configure_handlers(self):
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        for h in logging.root.handlers:
            h.addFilter(LoggerFilter())
            h.setFormatter(formatter)

    def __test_handler_connection(self, logger):
        try:
            logger.info("Test message sent to handlers")
        except Exception as e:
            print(f"Error sending log message: {e}")

    def setup(self):
        logger = self.__configure_logger()
        match self.handler_name:
            case "graylog":
                handler = GraylogHandler()
                logger.addHandler(handler)
            case "datadog":
                handler = DatadogHandler()
                logger.addHandler(handler)
        self.__configure_handlers()
        self.__test_handler_connection(logger)

    def get_dependency(self, worker_ctx):
        return logging.getLogger()
