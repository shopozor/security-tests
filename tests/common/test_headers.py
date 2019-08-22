import re
import requests
import sh


def test_security_headers_need_highest_possible_grade(domain):
    """
    Assess the security of our website according to securityheaders.com
    """

    res = requests.get('https://securityheaders.com/?q=' +
                       domain + '&followRedirects=on')
    assert res.headers['X-Grade'] == 'A+'


def test_ssllabs_scan_grade_is_highest(domain):
    """
    Assess the security of our website according to https://ssllabs.com/ssltest/
    """

    cmd = sh.Command('../../ssllabs-scan')
    result = cmd('-grade', domain)
    allMarks = re.findall('".*"\s*:\s*"(.?.?)"', result.stdout.decode("utf8"))
    assert len(allMarks) > 0
    for mark in allMarks:
        assert mark == 'A+'
