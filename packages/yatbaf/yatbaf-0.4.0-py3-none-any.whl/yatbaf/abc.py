from __future__ import annotations

__all__ = (
    "AbstractClient",
    "AbstractRouter",
)

from abc import ABC
from abc import abstractmethod
from typing import TYPE_CHECKING
from typing import Generic

from .typing import UpdateT

if TYPE_CHECKING:
    from collections.abc import AsyncIterator
    from collections.abc import Sequence
    from contextlib import AbstractAsyncContextManager

    from .handler import Handler
    from .models import HTTPResponse
    from .models import Request
    from .models import UpdateInfo
    from .typing import Middleware


class AbstractClient(ABC):
    """Abstract http client."""

    __slots__ = ()

    @abstractmethod
    async def send_post(
        self,
        request: Request,  # noqa: U100
        *,
        timeout: float | None = None  # noqa: U100
    ) -> HTTPResponse[bytes]:
        """Send POST request.

        :param request: :class:`~yatbaf.models.Request` object.
        :param timeout: Request timeout.
        """
        pass

    @abstractmethod
    def file_stream(
        self,
        url: str,  # noqa: U100
        chunk_size: int,  # noqa: U100
    ) -> AbstractAsyncContextManager[HTTPResponse[AsyncIterator[bytes]]]:
        """Download file content.

        :param url: File URL.
        :param chunk_size: Chunk length in bytes.
        """
        pass

    @abstractmethod
    async def close(self) -> None:
        pass


class AbstractRouter(ABC, Generic[UpdateT]):
    __slots__ = ()

    _parent: AbstractRouter[UpdateT] | None
    _middleware: list[Middleware[UpdateT]]

    @property
    @abstractmethod
    def _update_type(self) -> str:
        pass

    @abstractmethod
    def _register_routers(
        self, routers: Sequence[AbstractRouter[UpdateT]]
    ) -> None:
        pass

    @abstractmethod
    def _register_handlers(self, routers: Sequence[Handler[UpdateT]]) -> None:
        pass

    @abstractmethod
    def _on_registration(self) -> None:
        pass

    @abstractmethod
    async def _resolve(self, update: UpdateInfo, /) -> bool:
        pass
