# File: plugins/logger/providers/local.py

import logging, os
from ..base import LogProviderBase, LoggerFilter


class LocalProvider(LogProviderBase):
    def __create_handler(self):
        LOG_FILE = os.getenv("LOCAL_LOG_FILE")
        if LOG_FILE:
            handler = logging.FileHandler(LOG_FILE)
        else:
            handler = logging.StreamHandler()
        return handler

    def __test_provider_connection(self, logger):
        try:
            logger.info("Test message sent to Local")
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
