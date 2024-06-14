import logging, os
import pygelf
from ..base import LogProviderBase
from nameko.exceptions import ConfigurationError  # type: ignore


class GraylogProvider(LogProviderBase):
    def __create_handler(self):
        HOST = os.getenv("GRAYLOG_HOST")
        PORT = int(os.getenv("GRAYLOG_PORT", 12201))
        FACILITY = os.getenv("GRAYLOG_FACILITY", "my_service")

        if not all([HOST, PORT, FACILITY]):
            raise ConfigurationError(
                "Missing Graylog configuration environment variables."
            )

        handler = pygelf.GelfUdpHandler(host=HOST, port=PORT, facility=FACILITY)
        return handler

    def __test_provider_connection(self, logger):
        try:
            logger.info("Test message sent to Graylog")
        except Exception as e:
            print(f"Error sending log message: {e}")

    def setup(self):
        logger = self.configure_logger()
        handler = self.__create_handler()
        logger.addHandler(handler)
        self.configure_handlers()
        self.__test_provider_connection(logger)

    def get_logger(self):
        return logging.getLogger()
