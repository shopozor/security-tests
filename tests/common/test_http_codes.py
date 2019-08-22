import requests

from urllib.parse import urljoin


def test_non_existing_endpoint_returns_page_not_found(domain):
    endpoint = urljoin(domain, 'blabla')
    res = requests.get(endpoint)
    assert res.status_code == 404


def test_https_redirect(domain):
    """
    Tests that http is redirected to https
    """
   res = requests.get(domain, allow_redirects=False)
   assert res.status_code == 301
