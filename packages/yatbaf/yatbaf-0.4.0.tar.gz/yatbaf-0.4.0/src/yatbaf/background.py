from __future__ import annotations

__all__ = ("BackgroundTasks",)

import asyncio
import logging
from typing import TYPE_CHECKING
from typing import ParamSpec
from typing import final

if TYPE_CHECKING:
    from collections.abc import Coroutine

    from .typing import ErrorHandler

log = logging.getLogger(__name__)

P = ParamSpec("P")


@final
class BackgroundTasks:
    """Task manager."""

    __slots__ = (
        "_tasks",
        "_error_handler",
    )

    def __init__(self, error_handler: ErrorHandler, /) -> None:
        """
        :param error_handler: Error handler.
        """
        self._tasks: set[asyncio.Task] = set()
        self._error_handler = error_handler

    async def _wrapper(self, coro: Coroutine) -> None:
        try:
            await coro
        except Exception as error:
            await self._error_handler.on_error(error)

    def _create_task(self, coro: Coroutine, *, name: str | None = None) -> None:
        task = asyncio.create_task(coro, name=name)
        self._tasks.add(task)
        task.add_done_callback(self._tasks.discard)

    def add(self, coro: Coroutine, *, name: str | None = None) -> None:
        """Wrap the coroutine into a :class:`~asyncio.Task` and add to manager.

        :param coro: Coroutine to run as task.
        :param name: *Optional.* Task name.
        """
        self._create_task(self._wrapper(coro), name=name)

    @staticmethod
    async def kill(task: asyncio.Task, /) -> None:
        """Cancel task.

        :param task: :class:`~asyncio.Task` to be canceled.
        """
        if not task.done():
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass

    async def kill_all(self) -> None:
        """Cancel all tasks stored in manager."""
        while self._tasks:
            task = self._tasks.pop()
            await self.kill(task)

    async def wait_all(self) -> None:
        """Wait for all active tasks stored in manager."""
        if self._tasks:
            await asyncio.gather(*self._tasks)
