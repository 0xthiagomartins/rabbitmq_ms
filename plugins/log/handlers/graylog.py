import logging, os
import pygelf
from nameko.exceptions import ConfigurationError  # type: ignore


class GraylogHandler:

    def __init__(self):
        handler = self.__create_handler()
        return handler

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
