import logging
from abc import ABC, abstractmethod


class LogProviderBase(ABC):
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
