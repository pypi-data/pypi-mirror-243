from __future__ import annotations

__all__ = ("TelegramClient",)

import logging
from typing import TYPE_CHECKING
from typing import Literal
from typing import cast
from typing import final

import msgspec

from .enums import BotEnvi
from .exceptions import ChatMigratedError
from .exceptions import FileDownloadError
from .exceptions import FloodError
from .exceptions import InternalError
from .exceptions import MethodInvokeError
from .exceptions import TokenError
from .exceptions import WebhookConflictError
from .http import HttpClient
from .models import Request
from .models import ResponseError
from .types import ResponseParameters
from .utils import decode_error
from .utils import decode_response

if TYPE_CHECKING:
    from collections.abc import AsyncIterator
    from typing import Any
    from typing import Never

    from .abc import AbstractClient
    from .methods.abc import TelegramMethod
    from .models import ResponseOk
    from .types import File
    from .typing import ResultModelT

log = logging.getLogger(__name__)

SERVER_URL: Literal["https://api.telegram.org"] = "https://api.telegram.org"
"""Default api URL"""


class TelegramClient:
    """Telegram API client."""

    def __init__(
        self,
        token: str,
        *,
        api_url: str | None = None,
        environment: BotEnvi | None = None,
        client: AbstractClient | None = None,
    ) -> None:
        """
        :param token: API token.
        :param api_url: *Optional.* Api server address. Default to :attr:`SERVER_URL`.
        :param environment: *Optional.* Bot environment (see :class:`~yatbaf.enums.BotEnvi`).
        :param client: *Optional.* Http client.
        """  # noqa: E501
        self._client = HttpClient() if client is None else client
        self._api_url = SERVER_URL if api_url is None else api_url
        environment = BotEnvi.PROD if environment is None else environment
        self._creds = f"bot{token}" + (
            "/test" if environment is BotEnvi.TEST else ""
        )

    # yapf: disable
    @final
    async def invoke(
        self,
        method: TelegramMethod[ResultModelT], /, *,
        timeout: float | None = None,
        decoder: msgspec.json.Decoder[ResponseOk[ResultModelT]] | None = None,
    ) -> ResponseOk[ResultModelT]:
        """Invoke api method.

        See :ref:`methods`

        :param method: :class:`~yatbaf.methods.abc.TelegramMethod` instance.
        :param timeout: *Optional.* Request timeout.
        :param decoder: *Optional.* Response content decoder.
        """
        # yapf: enable
        url = f"{self._api_url}/{self._creds}"
        request = await self._prepare_request(url, method)
        response = await self._client.send_post(request, timeout=timeout)
        if response.status_code != 200:
            log.debug(
                f"Response status code: {response.status_code}, "
                f"content: {response.content!r}"
            )
            self._raise_for_status(response.content, method)
        return decode_response(method, response.content, decoder)

    @final
    async def download_file(
        self,
        file: File,
        chunk_size: int,
    ) -> AsyncIterator[bytes]:
        """Download file from Telegram servers.

        :param file: :class:`~yatbaf.types.file.File` instance
            (see :meth:`~yatbaf.bot.Bot.get_file`).
        :param chunk_size: Chunk length in bytes.
        """
        file_path = cast("str", file.file_path)
        url = f"{self._api_url}/file/{self._creds}/{file_path}"
        async with self._client.file_stream(url, chunk_size) as f:
            if f.status_code != 200:
                self._raise_for_status(b"".join([b async for b in f.content]))

            async for chunk in f.content:
                yield chunk

    @final
    @staticmethod
    async def _prepare_request(url: str, method: TelegramMethod) -> Request:
        """Build request.

        :param method: Method object.
        """
        content: bytes | None = None
        headers: dict[str, str] | None = None

        data, files = method._encode_params()

        # has files, data is `dict`
        if files is not None:
            data = cast("dict[str, Any]", data)
            for k, v in files.items():
                files[k] = (v.file_name, await v.read())

        # no files, data is `bytes`
        elif data is not None:
            content, data = cast("bytes", data), None
            headers = {"Content-Type": "application/json"}

        return Request(
            url=f"{url}/{method.__meth_name__}",
            content=content,
            method=method.__meth_name__,
            data=data,
            files=files,
            headers=headers,
        )

    async def close(self) -> None:
        """:meta private:"""
        log.debug("Shutting down")
        await self._client.close()

    @final
    @staticmethod
    def _raise_for_status(
        content: bytes,
        method: TelegramMethod | None = None,
    ) -> Never:
        """Raise request error. For internal use only.

        :param content: Raw response content.
        :param method: *Optional.* Method object.
        """
        response = decode_error(content)
        match response:
            case ResponseError(error_code=401):
                raise TokenError(response.description)
            case ResponseError(error_code=409):
                raise WebhookConflictError(response.description)
            # yapf: disable
            case ResponseError(parameters=ResponseParameters(retry_after=int(x))):  # noqa: E501
                raise FloodError(
                    method=cast("TelegramMethod", method),
                    error_code=response.error_code,
                    description=response.description,
                    retry_after=x,
                )
            case ResponseError(parameters=ResponseParameters(migrate_to_chat_id=int(x))):  # noqa: E501
                # yapf: enable
                raise ChatMigratedError(
                    method=cast("TelegramMethod", method),
                    error_code=response.error_code,
                    description=response.description,
                    migrate_to_chat_id=x,
                )
            case ResponseError(error_code=x) if x >= 500:
                raise InternalError(response.description)
            case _ if method is None:
                raise FileDownloadError(
                    error_code=response.error_code,
                    description=response.description,
                )

        raise MethodInvokeError(
            method=cast("TelegramMethod", method),
            error_code=response.error_code,
            description=response.description,
        )
