import logging
from plugins.logging.providers import GraylogDependency
from plugins.session import SessionDataDependency
from nameko.rpc import rpc
from nameko.events import (
    EventDispatcher,
    event_handler,
    BROADCAST,
    SINGLETON,
    SERVICE_POOL,
)


class ServiceA:
    name = "service_a"

    session_data: dict = SessionDataDependency()
    # logger: logging.Logger = GraylogDependency()
    dispatch = EventDispatcher()

    @rpc
    def sample_method(self, payload):
        return payload

    @rpc
    def dispatch_event(self, payload):
        self.dispatch("event_type", payload)

    @event_handler(
        "service_a", "event_type", handler_type=BROADCAST, reliable_delivery=False
    )
    def handle_event(self, payload):
        print(f"service received: {payload}")
