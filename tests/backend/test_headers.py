import pytest
import requests
import sh

# the Server header can give away important information to an attacker. other than that it doesn't bring anything useful
# therefore we should hide it


def test_server_header_not_returned(graphql_endpoint, query_me):
    res = requests.post(graphql_endpoint, json=query_me)
    with pytest.raises(KeyError):
        res.headers["Server"]


# this remains to be verified but I believe the X-Resolver-IP header is nginx specific and also doesn't do anything useful.
# this last fact needs to be verified. if that is the case though then we must make sure we are hiding it, because it gives
# away the fact that we are using nginx.
def test_ip_resolver_not_returned(graphql_endpoint, query_me):
    res = requests.post(graphql_endpoint, json=query_me)
    with pytest.raises(KeyError):
        res.headers["X-Resolver-IP"]

        
# HTTP Strict Transport Security
# this protects against protocol downgrade attacks (i.e. if an attacker can somehow make our https website
# run on the http protocol)
def test_hsts_present(graphql_endpoint, query_me):
    res = requests.post(graphql_endpoint, json=query_me)
    hsts = res.headers['Strict-Transport-Security']
    assert 'preload' in hsts
    assert 'includeSubDomains' in hsts


# CSP is one of the most modern security headers. it allows blocking a lot of unwanted things, it must be present
# and configured.
def test_csp_present(graphql_endpoint, query_me):
    res = requests.post(graphql_endpoint, json=query_me)
    csp = res.headers['Content-Security-Policy']
    # TODO test robustness e.g. things like unsafe-inline, ...
    assert csp.find('unsafe-inline') < 0
    # if we have csp, we may as well setup frame-ancestors
    assert csp.find("frame-ancestors 'none'") >= 0


# test click jacking protection. this effectively prevents other pages from rendering our website through the use of frame, iframes and object
# technically the XFO option is a bit older, the CSP version is more modern and allows setting up of the domains that might be allowed to render
# our page in an iframe, frame or object.
def test_click_jacking_protection(graphql_endpoint, query_me):
    res = requests.post(graphql_endpoint, json=query_me)
    try:
        csp = res.headers["Content-Security-Policy"]
        ancestor = csp.find("frame-ancestors 'none'")
        print('ancestor found at ', ancestor)
        assert ancestor > 0
    except KeyError:
        # ok csp not present, look for XFO
        assert res.headers['X-Frame-Options'] == "DENY"


# technically this one isn't needed if we have csp, csp with unsafe-inline protection already covers
# the problems solved by the X-XSS-Protection header, but it doesn't hurt to have it as well
def test_XSS_protection_present(graphql_endpoint, query_me):
    res = requests.post(graphql_endpoint, json=query_me)
    assert res.headers['X-XSS-Protection'].startswith('1; mode=block')


# Avoid MIME Sniffing Vulnerabilities
# MIME sniffing vulnerabilities can occur when a website allows users to upload data to the server.
# The vulnerability comes into play when an attacker disguises an HTML file as a different file type
# (e.g. a jpg, zip file, etc). Doing so would allow the attacker to successfully upload the file to
# the web server, assuming the web server accepts JPGs. Consequently, the browser will render it as
# an HTML file therefore providing the attacker with the possibility to execute XSS.
def test_content_type_options_present(graphql_endpoint, query_me):
    res = requests.post(graphql_endpoint, json=query_me)
    assert res.headers['X-Content-Type-Options'] == 'nosniff'


# unsafe things can happen with the referrer header, and this policy
# makes sure we never receive a downgraded (i.e. http) link
def test_referrer_policy_present(graphql_endpoint, query_me):
    res = requests.post(graphql_endpoint, json=query_me)
    assert res.headers['Referrer-Policy'] == 'strict-origin-when-cross-origin'


# Feature Policy will allow a site to enable or disable certain browser features and APIs in the
# interest of better security and privacy
def test_feature_policy_present(graphql_endpoint, query_me):
    res = requests.post(graphql_endpoint, json=query_me)
    fp = res.headers['Feature-Policy']


# Certificate Transparency
def test_expect_ct_present(graphql_endpoint, query_me):
    res = requests.post(graphql_endpoint, json=query_me)
    ct = res.headers['Expect-CT']

    
def test_security_headers_need_highest_possible_grade(domain):
    res = requests.get('https://securityheaders.com/?q=' +
                       domain + '&followRedirects=on')
    assert res.headers['X-Grade'] == 'A+'


def test_ssllabs_scan_grade_is_highest(domain):
    cmd = sh.Command('../../ssllabs-scan')
    result = cmd('-grade', domain)
    allMarks = re.findall('".*"\s*:\s*"(.?.?)"', result.stdout.decode("utf8"))
    assert len(allMarks) > 0
    for mark in allMarks:
        assert mark == 'A+'
