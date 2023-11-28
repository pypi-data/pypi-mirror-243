from __future__ import annotations

__all__ = ("HttpClient",)

import logging
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING
from typing import final

import httpx

from .abc import AbstractClient
from .exceptions import RequestTimeoutError
from .models import HTTPResponse
from .models import Request

if TYPE_CHECKING:
    from collections.abc import AsyncIterator
    from typing import Final

log = logging.getLogger(__name__)


@final
class HttpClient(AbstractClient):
    """Default http client."""

    __slots__ = ("_client",)

    def __init__(
        self,
        *,
        timeout: float = 8.0,
        connect_timeout: float = 16.0,
    ) -> None:
        """
        :param timeout: *Optional.* Request read/write timeout.
        :param connect_timeout: *Optional.* Request connect timeout.
        """
        self._client: Final[httpx.AsyncClient] = httpx.AsyncClient(
            timeout=httpx.Timeout(
                timeout=timeout,
                connect=connect_timeout,
            ),
        )

    async def send_post(
        self,
        request: Request, /,
        timeout: float | None = None,
    ) -> HTTPResponse[bytes]:  # yapf: disable
        try:
            response = await self._client.post(
                url=request.url,
                content=request.content,
                headers=request.headers,
                data=request.data,
                files=request.files,
                timeout=httpx.Timeout(
                    timeout=timeout,
                    connect=self._client.timeout.connect,
                ) if timeout is not None else httpx.USE_CLIENT_DEFAULT,
            )
        except httpx.TimeoutException as error:
            raise RequestTimeoutError(
                method=request.method,
                orig=error,
            ) from None

        return HTTPResponse(
            status_code=response.status_code,
            content=response.content,
        )

    @asynccontextmanager
    async def file_stream(
        self, url: str, chunk_size: int
    ) -> AsyncIterator[HTTPResponse[AsyncIterator[bytes]]]:
        try:
            async with self._client.stream("GET", url) as r:
                response = HTTPResponse(
                    status_code=r.status_code,
                    content=r.aiter_bytes(chunk_size),
                )
                yield response
        except httpx.TimeoutException as error:
            raise RequestTimeoutError(
                method="file",
                orig=error,
            ) from None

    async def close(self) -> None:
        log.debug("Shutting down")
        await self._client.aclose()
