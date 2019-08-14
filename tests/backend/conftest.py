import pytest
from urllib.parse import urljoin


def pytest_addoption(parser):
    parser.addoption(
        "--graphql-endpoint", action="store", default="graphql/", help="GraphQL endpoint url"
    )
    parser.addoption(
        "--domain", action="store", default="http://localhost:8000/", help="Domain to test"
    )


@pytest.fixture
def domain(request):
    return request.config.getoption("--domain")


@pytest.fixture
def graphql_endpoint(request):
    domain = request.config.getoption("--domain")
    endpoint = request.config.getoption("--graphql-endpoint")
    return urljoin(domain, endpoint)


@pytest.fixture
def query_me():
    return {"query": "query { me { id } }"}
