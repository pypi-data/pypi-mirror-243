import httpx
import pytest
import pytest_asyncio
from pytest_httpx import IteratorStream

from yatbaf.exceptions import RequestTimeoutError
from yatbaf.http import HttpClient
from yatbaf.models import Request
from yatbaf.telegram import SERVER_URL


@pytest.fixture
def request_json(token) -> Request:
    method = "sendmessage"
    return Request(
        url=f"{SERVER_URL}/bot{token}/{method}",
        method=method,
        content=b'{"chat_id":123,"text":"hello"}',
        headers={"Content-Type": "application/json"},
    )


@pytest.fixture
def request_file(token) -> Request:
    method = "senddocument"
    return Request(
        url=f"{SERVER_URL}/bot{token}/{method}",
        method=method,
        data={"chat_id": 123},
        files={"k": ("file.txt", b"hello\nworld")},
    )


@pytest_asyncio.fixture
async def client() -> HttpClient:
    client = HttpClient()
    yield client
    await client.close()


@pytest.mark.asyncio
async def test_client_post(token, httpx_mock, request_json, client):
    content = b'{"ok":true}'

    httpx_mock.add_response(
        method="POST",
        url=f"{SERVER_URL}/bot{token}/{request_json.method}",
        content=content,
    )

    result = await client.send_post(request_json)

    assert result.status_code == 200
    assert result.content == content


@pytest.mark.asyncio
async def test_client_stream(token, httpx_mock, client):
    content = [b'chunk' + str(x).encode() for x in range(5)]
    file_id = "qwerty1234"
    url = f"{SERVER_URL}/file/bot{token}/{file_id}"

    httpx_mock.add_response(
        url=url,
        stream=IteratorStream(content),
    )

    async with client.file_stream(url, len(content[0])) as f:
        assert f.status_code == 200
        assert [x async for x in f.content] == content


@pytest.mark.asyncio
async def test_client_timeout(httpx_mock, client, request_json):
    exception = httpx.ReadTimeout("timeout")
    httpx_mock.add_exception(exception)

    with pytest.raises(RequestTimeoutError) as error:
        await client.send_post(request_json)

    assert error.value.orig is exception
    assert error.value.method == request_json.method

    url = f"{SERVER_URL}/file/bot1234:qwer/1234"
    with pytest.raises(RequestTimeoutError) as error:
        async with client.file_stream(url, 64):
            pass

    assert error.value.orig is exception
    assert error.value.method == "file"
