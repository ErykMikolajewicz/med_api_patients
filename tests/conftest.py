import pytest
import httpx
from authlib.integrations.httpx_client import OAuth2Client


@pytest.fixture
def test_client():
    with httpx.Client(base_url="http://localhost:8008") as test_client:
        yield test_client


@pytest.fixture(scope='session')
def log_as():
    def log(login: str, password: str):
        authentication_client = OAuth2Client()
        token = authentication_client.fetch_token('http://127.0.0.1:8008/login/token', username=login,
                                                  password=password)
        return token

    yield log
