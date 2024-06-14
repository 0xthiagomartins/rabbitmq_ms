import logging
from plugins.logging.providers import GraylogDependency
from plugins.session import SessionDataDependency
from nameko.rpc import rpc


class MicroServiceA:
    name = "micro_service_A"

    session_data: dict = SessionDataDependency()
    logger: logging.Logger = GraylogDependency()

    @rpc
    def method_A(self, param1):
        pass
