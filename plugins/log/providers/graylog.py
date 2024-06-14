import logging, os
import pygelf
from ..base import LogProviderBase, LoggerFilter
from nameko.exceptions import ConfigurationError  # type: ignore


class GraylogProvider(LogProviderBase):
    def setup(self):
        logger = logging.getLogger()

        HOST = os.getenv("GRAYLOG_HOST")
        PORT = int(os.getenv("GRAYLOG_PORT", 12201))
        LOG_LEVEL = os.getenv("GRAYLOG_LOG_LEVEL", "INFO")
        FACILITY = os.getenv("GRAYLOG_FACILITY", "my_service")

        if not all([HOST, PORT, LOG_LEVEL, FACILITY]):
            raise ConfigurationError(
                "Missing Graylog configuration environment variables."
            )

        logger.setLevel(LOG_LEVEL)
        handler = pygelf.GelfUdpHandler(host=HOST, port=PORT, facility=FACILITY)
        logger.addHandler(handler)

        for h in logging.root.handlers:
            h.addFilter(LoggerFilter())

        self.__test_provider_connection(logger)

    def __test_provider_connection(self, logger):
        try:
            logger.info("Test message sent to Graylog")
        except Exception as e:
            print(f"Error sending log message: {e}")

    def get_logger(self):
        return logging.getLogger()
