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


def test_ssllabs_scan_grade_is_highest(domain):
    cmd = sh.Command('../../ssllabs-scan')
    result = cmd('-grade', '-json-flat', '-verbosity', 'error', domain)
    allMarks = re.findall('".*"\s*:\s*"(.?.?)"', result.stdout.decode("utf8"))
    assert len(allMarks) > 0
    for mark in allMarks:
      assert mark == 'A+'
