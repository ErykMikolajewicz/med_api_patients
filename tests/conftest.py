from asyncio import DefaultEventLoopPolicy, new_event_loop, set_event_loop

import pytest
import pytest_asyncio
import httpx
from authlib.integrations.httpx_client import AsyncOAuth2Client


@pytest.fixture(scope="session")
def event_loop_policy(request):
    loop = new_event_loop()
    set_event_loop(loop)
    return DefaultEventLoopPolicy()


@pytest_asyncio.fixture
async def test_client():
    async with httpx.AsyncClient(base_url="http://localhost:8008") as test_client:
        yield test_client


@pytest_asyncio.fixture(scope='session')
async def log_as():
    async def log(login: str, password: str):
        authentication_client = AsyncOAuth2Client()
        token = await authentication_client.fetch_token('http://127.0.0.1:8008/login/token', username=login,
                                                        password=password)
        return token

    yield log
