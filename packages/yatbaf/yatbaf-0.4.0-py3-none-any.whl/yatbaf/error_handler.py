from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .typing import ErrorHandler

log = logging.getLogger(__name__)


class DefaultErrorHandler:

    def __init__(self, error_handler: ErrorHandler | None = None) -> None:
        self._error_handler = error_handler

    def _log(self, message: str, error: Exception) -> None:
        log.error(f"{message}: {error}")
        log.debug("Exception traceback:", exc_info=error)

    async def on_error(self, error: Exception) -> None:
        if self._error_handler is None:
            self._log("Unexcpected error.", error)
            return

        try:
            await self._error_handler.on_error(error)
        except Exception as error:
            self._log(f"Unexcpected error in {self._error_handler!r}.", error)
