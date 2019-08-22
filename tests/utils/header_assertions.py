import requests


def assert_no_server_header(response):
    assert 'Server' not in response.headers


def assert_no_x_resolver_ip_header(response):
    assert 'X-Resolver-IP' not in response.headers


def assert_hsts_present(response):
    hsts = response.headers['Strict-Transport-Security']
    assert 'preload' in hsts
    assert 'includeSubDomains' in hsts


def assert_csp_present(response):
    csp = response.headers['Content-Security-Policy']
    # TODO test robustness e.g. things like unsafe-inline, ...
    assert csp.find('unsafe-inline') < 0
    # if we have csp, we may as well setup frame-ancestors
    assert csp.find("frame-ancestors 'none'") >= 0


def assert_click_jacking_protection(response):
    try:
        csp = response.headers["Content-Security-Policy"]
        ancestor = csp.find("frame-ancestors 'none'")
        assert ancestor > 0
    except KeyError:
        # ok csp not present, look for XFO
        assert response.headers['X-Frame-Options'] == "DENY"


def assert_XSS_protection_present(response):
    assert response.headers['X-XSS-Protection'].startswith('1; mode=block')


def assert_content_type_options_present(response):
    assert response.headers['X-Content-Type-Options'] == 'nosniff'


def assert_referrer_policy_present(response):
    assert response.headers['Referrer-Policy'] == 'strict-origin-when-cross-origin'


def assert_feature_policy_present(response):
    assert 'Feature-Policy' in response.headers


def assert_expect_ct_present(response):
    assert 'Expect-CT' in response.headers
