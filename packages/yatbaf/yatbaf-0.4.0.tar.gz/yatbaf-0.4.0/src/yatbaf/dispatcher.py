from __future__ import annotations

__all__ = ("Dispatcher",)

import logging
from collections import defaultdict
from typing import TYPE_CHECKING
from typing import Any

from .background import BackgroundTasks
from .enums import BotEnvi
from .error_handler import DefaultErrorHandler
from .models import UpdateInfo
from .router import BaseRouter
from .router import router_map
from .telegram import TelegramClient
from .utils import decode_webhook
from .utils import extract_bot_id

if TYPE_CHECKING:
    from collections.abc import Sequence

    from .abc import AbstractClient
    from .abc import AbstractRouter
    from .handler import Handler
    from .methods.abc import TelegramMethod
    from .types import Update
    from .typing import Context
    from .typing import ErrorHandler
    from .typing import Guard
    from .typing import Middleware
    from .typing import ResultModelT
    from .typing import UpdateModel

log = logging.getLogger(__name__)


class Dispatcher(BaseRouter):
    """Dispatcher"""

    __slots__ = (
        "_api_client",
        "_error_handler",
        "_tasks",
        "_id",
        "_routers",
        "_ctx",
    )

    def __init__(
        self,
        token: str,
        handlers: Sequence[Handler] | None = None,
        routers: Sequence[AbstractRouter] | None = None,
        middleware: Sequence[Middleware] | None = None,
        guards: Sequence[Guard] | None = None,
        context: Context[UpdateModel] | None = None,
        error_handler: ErrorHandler | None = None,
        api_url: str | None = None,
        environment: BotEnvi | None = None,
        client: AbstractClient | None = None,
    ) -> None:
        """
        :param middleware: *Optional.* A sequence of :class:`~yatbaf.typing.Middleware`.
        :param guards: *Optional.* A sequence of :class:`~yatbaf.typing.Guard`.
        :param handlers: *Optional.* A sequence of :class:`~yatbaf.handler.Handler`.
        :param routers: *Optional.* A sequence of :class:`~yatbaf.abc.AbstractRouter`.
        :param context: *Optional.* :class:`~yatbaf.typing.Context` function.
        :param api_url: *Optional.* Api server address. Defautl to :attr:`~yatbaf.telegram.SERVER_URL`.
        :param environment: *Optional.* Bot environment (see :class:`~yatbaf.enums.BotEnvi`).
        :param client: *Optional.* Http client.
        """  # noqa: E501
        self._api_client = TelegramClient(
            token=token,
            api_url=api_url,
            environment=environment,
            client=client,
        )
        self._error_handler = DefaultErrorHandler(error_handler)
        self._tasks = BackgroundTasks(self._error_handler)
        self._routers: dict[str, list[AbstractRouter]] = {
            "message": [],
            "edited_message": [],
            "channel_post": [],
            "edited_channel_post": [],
            "inline_query": [],
            "chosen_inline_result": [],
            "callback_query": [],
            "shipping_query": [],
            "pre_checkout_query": [],
            "poll": [],
            "poll_answer": [],
            "my_chat_member": [],
            "chat_member": [],
            "chat_join_request": [],
        }
        self._id = extract_bot_id(token)
        self._ctx: dict[str, Any] = {}

        super().__init__(
            routers=routers,
            handlers=handlers,
            middleware=middleware,
            guards=guards,
            context=context,
        )

    @property
    def id(self) -> int:  # noqa: A003
        """Bot ID"""
        return self._id

    @property
    def ctx(self) -> dict[str, Any]:
        """Dict object.

        Use it to store extra state on bot instance.
        """
        return self._ctx

    @property
    def tasks(self) -> BackgroundTasks:
        """Task manager."""
        return self._tasks

    @property
    def _update_type(self) -> str:
        raise RuntimeError(
            "Dispatcher can't be used here. "
            "You are trying to do something illegal ._."
        )

    def _register_routers(self, routers: Sequence[AbstractRouter]) -> None:
        for router in routers:
            if router._parent is None:
                self._routers[router._update_type].append(router)
                router._parent = self
                router._on_registration()

            elif router._parent is not self:
                raise ValueError(
                    f"{router} already registered in {router._parent}"
                )

    def _register_handlers(self, handlers: Sequence[Handler]) -> None:
        routers: dict[str, list[Handler]] = defaultdict(list)
        for handler in handlers:
            routers[handler.update_type].append(handler)

        self._register_routers([
            router_map[t](handlers=h) for t, h in routers.items()
        ])

    def _bind_self(self, update: ResultModelT, /) -> ResultModelT:
        raise NotImplementedError()

    def _on_registration(self) -> None:
        pass

    async def _call_api(
        self, method: TelegramMethod[ResultModelT]
    ) -> ResultModelT:
        """:meta private:"""
        return self._bind_self((await self._api_client.invoke(method)).result)

    async def _resolve(self, update: UpdateInfo, /) -> bool:
        """:meta private:"""
        content = update.content
        async with self._context(content):
            if await self._check_guards(content):
                routers = self._routers[update.name]
                for router in routers:
                    if await router._resolve(update):
                        return True
        return False

    async def process_update(self, data: Update | bytes, /) -> None:
        """Process incoming update.

        :param data: :class:`~yatbaf.types.update.Update` instance (long
            polling) or :class:`bytes` (webhook content).
        """
        # catch any exceptions in context/guard/middleware/handler
        try:
            if isinstance(data, bytes):
                data = decode_webhook(data)

            content, name = data.filter()
            await self._resolve(
                UpdateInfo(
                    id=data.update_id,
                    name=name,
                    content=self._bind_self(content),
                )
            )

        except Exception as error:
            await self._error_handler.on_error(error)

    async def shutdown(self, force: bool = False) -> None:
        """Cleanup resources.

        :param force: Pass ``True`` if you want to cancel all active tasks
            stored in :attr:`.tasks`.
        """
        log.debug("bot shutting down...")
        if not force:
            # wait for active tasks
            await self._tasks.wait_all()
        else:
            await self._tasks.kill_all()
        # close http client
        await self._api_client.close()
