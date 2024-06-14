import pytest
from nameko.standalone.rpc import ClusterRpcProxy
from src.config import config

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
    pass


def test_proxy_dispatch_event():
    pass
