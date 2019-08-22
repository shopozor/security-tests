import pytest
from urllib.parse import urljoin


def pytest_addoption(parser):
    parser.addoption(
        "--domain", action="store", default="http://localhost:8000/", help="Domain to test"
    )


@pytest.fixture
def domain(request):
    return request.config.getoption("--domain")
