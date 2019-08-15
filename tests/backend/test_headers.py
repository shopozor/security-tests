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


def test_hsts_present(graphql_endpoint, query_me):
    res = requests.post(graphql_endpoint, json=query_me)
    hsts = res.headers['Strict-Transport-Security']
    assert 'preload' in hsts
    assert 'includeSubDomains' in hsts


def test_csp_present(graphql_endpoint, query_me):
    res = requests.post(graphql_endpoint, json=query_me)
    csp = res.headers['Content-Security-Policy']
    # TODO test robustness e.g. things like unsafe inlines, ...


def test_XFO_present(graphql_endpoint, query_me):
    res = requests.post(graphql_endpoint, json=query_me)
    assert res.headers['X-Frame-Options'] == "DENY"


def test_XSS_protection_present(graphql_endpoint, query_me):
    res = requests.post(graphql_endpoint, json=query_me)
    assert res.headers['X-XSS-Protection'].startswith('1; mode=block')


def test_content_type_options_present(graphql_endpoint, query_me):
    res = requests.post(graphql_endpoint, json=query_me)
    assert res.headers['X-Content-Type-Options'] == 'nosniff'


def test_referrer_policy_present(graphql_endpoint, query_me):
    res = requests.post(graphql_endpoint, json=query_me)
    assert res.headers['Referrer-Policy'] == 'strict-origin-when-cross-origin'


def test_feature_policy_present(graphql_endpoint, query_me):
    res = requests.post(graphql_endpoint, json=query_me)
    fp = res.headers['Feature-Policy']

# TODO expect-ct
# def test_expect_ct_present(graphql_endpoint, query_me):
