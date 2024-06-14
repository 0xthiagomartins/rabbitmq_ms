from nameko.standalone.events import event_dispatcher


class ClusterEventDispatcherProxy:
    def __init__(self, config):
        self.config = config

    def __enter__(self):
        self.dispatch = event_dispatcher()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def dispatch_event(self, service_name, event_type, payload):
        self.dispatch(service_name, event_type, payload)
