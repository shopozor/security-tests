import pytest
import requests
import sh


def test_server_header_not_returned(domain):
    """
    The Server header can give away important information to an attacker.
    Other than that it doesn't bring anything useful. Therefore we should hide it.  
    """

    res = request.get(domain)
    pytest.helpers.tests.common.headers.test_server_header_not_returned(res)


def test_ip_resolver_not_returned(domain):
    """
    This remains to be verified but I believe the X-Resolver-IP header is nginx-specific and also doesn't do anything useful.
    This last fact needs to be verified. If that is the case though then we must make sure we are hiding it, because it gives
    away the fact that we are using nginx.
    """

    res = request.get(domain)
    pytest.helpers.tests.common.headers.test_ip_resolver_not_returned(res)


def test_hsts_present(domain):
    """
    HTTP Strict Transport Security
    This protects against protocol downgrade attacks (i.e. if an attacker can somehow make our https website
    run on the http protocol)
    """

    res = request.get(domain)
    pytest.helpers.tests.common.headers.test_hsts_present(res)


def test_csp_present(domain):
    """
    CSP is one of the most modern security headers. it allows blocking a lot of unwanted things, it must be present
    and configured.
    """

    res = request.get(domain)
    pytest.helpers.tests.common.headers.test_csp_present(res)


def test_click_jacking_protection(domain):
    """
    Test click jacking protection. This effectively prevents other pages from rendering our website through the use of frame, iframes and object
    technically the XFO option is a bit older, the CSP version is more modern and allows setting up of the domains that might be allowed to render
    our page in an iframe, frame or object.
    """

    res = request.get(domain)
    pytest.helpers.tests.common.headers.test_click_jacking_protection(res)


def test_XSS_protection_present(domain):
    """
    Technically this one isn't needed if we have csp, csp with unsafe-inline protection already covers
    the problems solved by the X-XSS-Protection header, but it doesn't hurt to have it as well
    """

    res = request.get(domain)
    pytest.helpers.tests.common.headers.test_XSS_protection_present(res)


def test_content_type_options_present(domain):
    """
    Avoid MIME Sniffing Vulnerabilities
    MIME sniffing vulnerabilities can occur when a website allows users to upload data to the server.
    The vulnerability comes into play when an attacker disguises an HTML file as a different file type
    (e.g. a jpg, zip file, etc). Doing so would allow the attacker to successfully upload the file to
    the web server, assuming the web server accepts JPGs. Consequently, the browser will render it as
    an HTML file therefore providing the attacker with the possibility to execute XSS.
    """
    res = request.get(domain)
    pytest.helpers.tests.common.headers.test_content_type_options_present(res)


def test_referrer_policy_present(domain):
    """
    Unsafe things can happen with the referrer header, and this policy
    makes sure we never receive a downgraded (i.e. http) link
    """

    res = request.get(domain)
    pytest.helpers.tests.common.headers.test_referrer_policy_present(res)


def test_feature_policy_present(domain):
    """ 
    Feature Policy will allow a site to enable or disable certain browser features and APIs in the
    interest of better security and privacy
    """

    res = request.get(domain)
    pytest.helpers.tests.common.headers.test_feature_policy_present(res)


def test_expect_ct_present(domain):
    """
    Certificate Transparency
    """

    res = request.get(domain)
    pytest.helpers.tests.common.headers.test_expect_ct_present(res)
