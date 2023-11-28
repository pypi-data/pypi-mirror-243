import pytest
import pytest_asyncio
from pytest_httpx import IteratorStream

from yatbaf.exceptions import ChatMigratedError
from yatbaf.exceptions import FileDownloadError
from yatbaf.exceptions import FloodError
from yatbaf.exceptions import InternalError
from yatbaf.exceptions import MethodInvokeError
from yatbaf.exceptions import TokenError
from yatbaf.exceptions import WebhookConflictError
from yatbaf.http import HttpClient
from yatbaf.methods import GetMe
from yatbaf.methods import SendDocument
from yatbaf.methods import SendMessage
from yatbaf.models import Request
from yatbaf.models import ResponseOk
from yatbaf.telegram import SERVER_URL
from yatbaf.telegram import TelegramClient
from yatbaf.types import File
from yatbaf.types import User

TOKEN = "123456789:totkentest"
URL = f"{SERVER_URL}/bot{TOKEN}"


@pytest_asyncio.fixture
async def tg() -> TelegramClient:
    tg_client = TelegramClient(
        token=TOKEN,
        client=HttpClient(),
    )
    yield tg_client
    await tg_client.close()


@pytest.fixture
def json_error():
    return {
        "ok": False,
        "description": "description",
        "error_code": 400,
    }


@pytest.mark.asyncio
async def test_prepare_request_empty():
    method = GetMe()
    req = await TelegramClient._prepare_request(URL, method)
    assert req == Request(
        url=f"{URL}/{method.__meth_name__}",
        content=None,
        method=str(method),
        data=None,
        files=None,
        headers=None,
    )


@pytest.mark.asyncio
async def test_prepare_request():
    method = SendMessage(text="ping", chat_id=12345)
    req = await TelegramClient._prepare_request(URL, method)
    assert req == Request(
        url=f"{URL}/{method.__meth_name__}",
        content=method._encode_params()[0],
        method=str(method),
        data=None,
        files=None,
        headers={"Content-Type": "application/json"},
    )


@pytest.mark.asyncio
async def test_prepare_request_file_content():

    class Doc:
        file_name = "file.txt"

        async def read(self):
            return b"content"

    document = Doc()

    method = SendDocument(document=document, chat_id=12345)
    req = await TelegramClient._prepare_request(URL, method)
    fn = method.document
    assert req == Request(
        url=f"{URL}/{method.__meth_name__}",
        content=None,
        method=str(method),
        data={
            "chat_id": 12345,
            "document": fn,
        },
        files={fn.split("//")[1]: ("file.txt", b"content")},
        headers=None,
    )


@pytest.mark.asyncio
async def test_prepare_request_file_id():
    document = "fileid"
    method = SendDocument(document=document, chat_id=12345)
    req = await TelegramClient._prepare_request(URL, method)
    assert req == Request(
        url=f"{URL}/{method.__meth_name__}",
        content=method._encode_params()[0],
        method=str(method),
        data=None,
        files=None,
        headers={"Content-Type": "application/json"},
    )


@pytest.mark.asyncio
async def test_invoke(httpx_mock, tg):
    json = {
        "ok": True,
        "result": {
            "id": 123456789,
            "is_bot": True,
            "first_name": "Test First Name",
        },
    }
    httpx_mock.add_response(method="POST", url=f"{URL}/getme", json=json)
    resp = await tg.invoke(GetMe())

    assert isinstance(resp, ResponseOk)
    assert isinstance(resp.result, User)
    assert resp.result.id == json["result"]["id"]
    assert resp.result.is_bot


@pytest.mark.asyncio
async def test_file_stream(httpx_mock, tg):
    content = b"hello world"
    httpx_mock.add_response(
        method="GET",
        url=f"{SERVER_URL}/file/bot{TOKEN}/123",
        stream=IteratorStream([content]),
    )
    gen = tg.download_file(
        File(file_id=123, file_unique_id="123", file_path="123"),
        chunk_size=64 * 1024,
    )
    file = b"".join([x async for x in gen])
    assert file == content


@pytest.mark.asyncio
async def test_token_error(httpx_mock, tg, json_error):
    status = 401
    json_error["error_code"] = status

    httpx_mock.add_response(
        method="POST",
        status_code=status,
        json=json_error,
    )

    with pytest.raises(TokenError):
        await tg.invoke(GetMe())


@pytest.mark.asyncio
async def test_webhook_error(httpx_mock, tg, json_error):
    status = 409
    json_error["error_code"] = status

    httpx_mock.add_response(
        method="POST",
        status_code=status,
        json=json_error,
    )

    with pytest.raises(WebhookConflictError):
        await tg.invoke(GetMe())


@pytest.mark.asyncio
async def test_flood_error(httpx_mock, tg, json_error):
    status = 429
    json_error["error_code"] = status
    json_error["parameters"] = {"retry_after": 123}

    httpx_mock.add_response(
        method="POST",
        status_code=status,
        json=json_error,
    )

    method = GetMe()
    with pytest.raises(FloodError) as error:
        await tg.invoke(method)

    assert error.value.retry_after == 123
    assert error.value.method is method


@pytest.mark.asyncio
async def test_chat_migrated_error(httpx_mock, tg, json_error):
    status = 400
    json_error["error_code"] = status
    json_error["parameters"] = {"migrate_to_chat_id": 123}

    httpx_mock.add_response(
        method="POST",
        status_code=status,
        json=json_error,
    )

    method = GetMe()
    with pytest.raises(ChatMigratedError) as error:
        await tg.invoke(method)

    assert error.value.migrate_to_chat_id == 123
    assert error.value.method is method


@pytest.mark.asyncio
async def test_file_error(httpx_mock, tg, json_error):
    status = 400
    json_error["error_code"] = status

    httpx_mock.add_response(
        method="GET",
        status_code=status,
        json=json_error,
    )

    with pytest.raises(FileDownloadError) as error:
        gen = tg.download_file(
            File(file_id=123, file_unique_id="123"),
            chunk_size=64 * 1024,
        )
        async for x in gen:
            pass

    assert error.value.error_code == status
    assert error.value.description == json_error["description"]


@pytest.mark.asyncio
async def test_internal_error(httpx_mock, tg, json_error):
    status = 500
    json_error["error_code"] = status

    httpx_mock.add_response(
        method="POST",
        status_code=status,
        json=json_error,
    )

    with pytest.raises(InternalError):
        await tg.invoke(GetMe())


@pytest.mark.asyncio
async def test_method_error(httpx_mock, tg, json_error):
    status = 400
    json_error["error_code"] = status

    httpx_mock.add_response(
        method="POST",
        status_code=status,
        json=json_error,
    )

    method = GetMe()
    with pytest.raises(MethodInvokeError) as error:
        await tg.invoke(method)

    assert error.value.method is method
    assert error.value.error_code == status
    assert error.value.description == json_error["description"]
