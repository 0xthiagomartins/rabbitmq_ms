import pytest
from nameko.standalone.rpc import ClusterRpcProxy
from src.config import config
from plugins import ClusterEventDispatcherProxy

config = {"AMQP_URI": config}


def test_rpc_call_sync():
    payload = "test"
    with ClusterRpcProxy(config) as rpc:
        rpc.service_a.dispatch_event(payload)


def test_rpc_call_async():
    payload = "test"
    with ClusterRpcProxy(config) as rpc:
        response = rpc.service_a.sample_method.call_async(payload)
        # do something
        response = response.result()
    assert response == payload


def test_envvars():
    assert config["AMQP_URI"] is not None


# Usage in your tests
def test_dispatch_event():
    payload = "test"
    with ClusterEventDispatcherProxy(config) as dispatcher:
        dispatcher.dispatch("service_a", "event_type", payload)
        # Add assertions here if there are any side effects to check


if __name__ == "__main__":
    pytest.main()
