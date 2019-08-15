import pytest
import requests
import sh


def test_server_header_not_returned(graphql_endpoint, query_me):
    res = requests.post(graphql_endpoint, json=query_me)
    with pytest.raises(KeyError):
        res.headers["Server"]


def test_ip_resolver_not_returned(graphql_endpoint, query_me):
    res = requests.post(graphql_endpoint, json=query_me)
    with pytest.raises(KeyError):
        res.headers["X-Resolver-IP"]


def test_security_headers_need_highest_possible_grade(domain):
    res = requests.get('https://securityheaders.com/?q=' +
                       domain + '&followRedirects=on')
    assert res.headers['X-Grade'] == 'A+'


def test_ssllabs_scan_grade_is_highest(graphql_endpoint):
    cmd = sh.Command('../../ssllabs-scan')
    result = cmd('-grade', 'http://www.softozor.ch')
    # TODO: assert grade is A+
    # result is --> "http://www.softozor.ch": "A"
