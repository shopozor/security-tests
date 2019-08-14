import pytest
import requests


def test_server_header_not_returned(graphql_endpoint, query_me):
    res = requests.post(graphql_endpoint, json=query_me)
    with pytest.raises(KeyError):
        res.headers["Server"]


def test_ip_resolver_not_returned(graphql_endpoint, query_me):
    res = requests.post(graphql_endpoint, json=query_me)
    with pytest.raises(KeyError):
        res.headers["X-Resolver-IP"]
