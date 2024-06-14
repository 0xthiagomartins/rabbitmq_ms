import logging, os
from abc import ABC, abstractmethod
from nameko.exceptions import ConfigurationError  # type: ignore


class LogHandlerBase(ABC):

    def configure_logger(self):
        logger = logging.getLogger()
        LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
        if not all([LOG_LEVEL]):
            raise ConfigurationError(
                "Missing Basic Log configuration environment variables."
            )
        logger.setLevel(LOG_LEVEL)

        return logger

    def configure_handlers(self):
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        for h in logging.root.handlers:
            h.addFilter(LoggerFilter())
            h.setFormatter(formatter)

    @abstractmethod
    def setup(self):
        pass

    @abstractmethod
    def get_logger(self):
        pass


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
