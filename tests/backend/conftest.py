import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--endpoint", action="store", default="http://localhost:8000/graphql/", help="GraphQL endpoint url"
    )


@pytest.fixture
def graphql_endpoint(request):
    return request.config.getoption("--endpoint")
