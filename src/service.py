import logging
from plugins.log import LoggerDependencyProvider
from plugins.session import SessionDataDependency
from nameko.rpc import rpc  # type: ignore
from nameko.timer import timer  # type: ignore
from nameko.events import (  # type: ignore
    EventDispatcher,
    event_handler,
    BROADCAST,
    SINGLETON,
    SERVICE_POOL,
)


class Service:
    name = "service_a"

    session_data: dict = SessionDataDependency()
    logger: logging.Logger = LoggerDependencyProvider()
    dispatch = EventDispatcher()

    @rpc
    def sample_method(self, payload):
        """Returns the payload received."""
        return payload

    @rpc
    def dispatch_event(self, payload):
        """Dispatches an event of type 'event_type' with the given payload."""
        self.dispatch("event_type", payload)

    @event_handler(
        "service_a", "event_type", handler_type=BROADCAST, reliable_delivery=False
    )
    def handle_event_broadcast(self, payload):
        """
        Handles events of type 'event_type' using BROADCAST.

        BROADCAST handler type sends the event to all instances of the service.
        """
        print(f"Broadcast handler received: {payload}")

    @event_handler(
        "service_a", "event_type", handler_type=SINGLETON, reliable_delivery=True
    )
    def handle_event_singleton(self, payload):
        """
        Handles events of type 'event_type' using SINGLETON.

        SINGLETON handler type ensures only one instance of the service handles the event.
        """
        print(f"Singleton handler received: {payload}")

    @event_handler(
        "service_a", "event_type", handler_type=SERVICE_POOL, reliable_delivery=True
    )
    def handle_event_service_pool(self, payload):
        """
        Handles events of type 'event_type' using SERVICE_POOL.

        SERVICE_POOL handler type distributes events among instances of the service based on a pool.
        """
        print(f"Service pool handler received: {payload}")

    @event_handler(
        "service_a",
        "another_event_type",
        handler_type=BROADCAST,
        reliable_delivery=False,
    )
    def handle_another_event(self, payload):
        """
        Handles events of type 'another_event_type' using BROADCAST.

        BROADCAST handler type sends the event to all instances of the service.
        """
        print(f"Another event received: {payload}")
