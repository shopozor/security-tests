import pytest
import requests


def test_server_header(graphql_endpoint):
    res = requests.post(graphql_endpoint, json={
                        "query": "query { me { id } }"})
    with pytest.raises(KeyError):
        res.headers["Server"]


def test_ip_resolver(graphql_endpoint):
    res = requests.post(graphql_endpoint, json={
                        "query": "query { me { id } }"})
    with pytest.raises(KeyError):
        res.headers["X-Resolver-IP"]
