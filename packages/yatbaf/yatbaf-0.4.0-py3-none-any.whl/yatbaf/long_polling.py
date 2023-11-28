from __future__ import annotations

__all__ = ("LongPolling",)

import asyncio
import logging
import signal
from typing import TYPE_CHECKING
from typing import Any
from typing import cast

from httpx import ConnectError

from .enums import UpdateType
from .exceptions import RequestTimeoutError
from .methods import GetUpdates

if TYPE_CHECKING:
    from collections.abc import Iterable

    from .bot import Bot
    from .types import Update
    from .typing import PollingHook

log = logging.getLogger(__name__)

# TODO: windows?
SIGNALS = (signal.SIGINT, signal.SIGTERM)


class LongPolling:
    """Long polling runner."""

    __slots__ = (
        "_bot",
        "_event",
        "_method",
        "_running",
        "_on_startup",
        "_on_shutdown",
        "_connection_delay",
        "_timeout_delay",
    )

    def __init__(
        self,
        bot: Bot,
        /,
        timeout: float = 60.0,
        offset: int | None = None,
        limit: int | None = None,
        allowed_updates: list[UpdateType] | None = None,
        on_startup: Iterable[PollingHook] | None = None,
        on_shutdown: Iterable[PollingHook] | None = None,
        connection_delay: int = 20,
        timeout_delay: int = 5,
    ) -> None:
        """
        :param bot: :class:`~yatbaf.bot.Bot` isinstance.
        :param timeout: *Optional.* Timeout in seconds for long polling. Should
            be positive, short polling should be used for testing purposes only.
        :param offset: *Optional.* Identifier of the first update to be
            returned. Must be greater by one than the highest among the
            identifiers of previously received updates. By default, updates
            starting with the earliest unconfirmed update are returned. An
            update is considered confirmed as soon as getUpdates is called with
            an offset higher than its ``update_id``. The negative offset can be
            specified to retrieve updates starting from -offset update from the
            end of the updates queue. All previous updates will be forgotten.
        :param limit: *Optional.* Limits the number of updates to be retrieved.
            Values between 1-100 are accepted. Defaults to 100.
        :param allowed_updates: *Optional.* A list of the update types you want
            your bot to receive. See :class:`~yatbaf.enums.UpdateType` for a
            complete list of available update types. Specify an empty list to
            receive all update types except ``chat_member`` (default). If not
            specified, the previous setting will be used.
        :param on_startup: *Optional.* A sequence of
            :class:`~yatbaf.typing.PollingHook` to run on polling startup.
        :param on_shutdown: *Optional.* A sequence of
            :class:`~yatbaf.typing.PollingHook` to run on polling shutdown.
        :param connection_delay: *Optional.* Retry delay on request errors.
            Default 20 sec.
        :param timeout_delay: *Optional.* Retry delay on timeout error.
            Default 5 sec.


        .. note::

            ``allowed_updates`` doesn't affect updates created before the call
            to the :meth:`start`, so unwanted updates may be received for a
            short period of time.

        .. warning::

            Long polling will not work if an outgoing webhook is set up.
        """
        self._method = GetUpdates(
            timeout=timeout,
            offset=offset,
            limit=limit,
            allowed_updates=allowed_updates,
        )
        self._bot = bot
        self._event = asyncio.Event()
        self._running = False
        self._on_startup = on_startup if on_startup is not None else []
        self._on_shutdown = on_shutdown if on_shutdown is not None else []
        self._connection_delay = connection_delay
        self._timeout_delay = timeout_delay

    async def _get_updates(self, queue: asyncio.Queue) -> None:
        timeout = cast("float", self._method.timeout) + 5.0
        while not self._event.is_set():
            try:
                updates: list[Update] = (
                    await self._bot._api_client.invoke(
                        self._method,
                        timeout=timeout,
                    )
                ).result

                if updates:
                    self._method.offset = updates[-1].update_id + 1
                    queue.put_nowait(updates)

            except (ConnectError, RequestTimeoutError) as error:
                if isinstance(error, RequestTimeoutError):
                    message = (
                        "Connection timed out. "
                        f"Next try in {self._timeout_delay} sec."
                    )
                    delay = self._timeout_delay
                else:
                    message = (
                        "Network connection error. "
                        f"Next try in {self._connection_delay} sec."
                    )
                    delay = self._connection_delay

                log.error(message)
                await asyncio.sleep(delay)

            except Exception as error:
                self._event.set()
                await self._bot._error_handler.on_error(error)

    async def _main_loop(self) -> None:
        log.info("Starting long polling...")
        queue: asyncio.Queue = asyncio.Queue()
        updates_task = asyncio.create_task(self._get_updates(queue))

        bot = self._bot
        while not self._event.is_set():
            try:
                for update in (await asyncio.wait_for(queue.get(), 0.2)):
                    bot.tasks._create_task(
                        bot.process_update(update),
                        name=f"update-task-{update.update_id}",
                    )
            except TimeoutError:
                pass

        await bot.tasks.kill(updates_task)

    async def _startup(self) -> None:
        log.debug("Sturtup...")
        if self._running:
            return
        self._event.clear()

        for func in self._on_startup:
            await func(self._bot)

        loop = asyncio.get_running_loop()
        for s in SIGNALS:
            loop.add_signal_handler(s, self.stop)
        self._running = True

    async def _shutdown(self) -> None:
        log.debug("Shutdown...")
        if not self._running:
            return
        self._running = False

        await self._bot.tasks.wait_all()
        try:
            for func in self._on_shutdown:
                await func(self._bot)
        finally:
            await self._bot.shutdown()

    async def _run(self) -> None:
        try:
            await self._startup()
        except Exception as error:
            log.error("Startup failed.", exc_info=error)
            return

        await self._main_loop()
        await self._shutdown()

    def start(self) -> None:
        """Start long polling"""
        asyncio.run(self._run())

    def stop(self, *args: Any) -> None:  # noqa: U100
        """Stop long polling"""
        self._event.set()
