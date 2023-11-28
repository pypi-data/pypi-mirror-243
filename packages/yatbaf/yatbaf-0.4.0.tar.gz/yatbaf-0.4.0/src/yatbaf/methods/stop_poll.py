from __future__ import annotations

from typing import TYPE_CHECKING
from typing import final

from yatbaf.types import Poll

from .abc import TelegramMethod

if TYPE_CHECKING:
    from yatbaf.types import InlineKeyboardMarkup


@final
class StopPoll(TelegramMethod[Poll]):
    """See :meth:`yatbaf.bot.Bot.stop_poll`"""

    chat_id: str | int
    message_id: int
    reply_markup: InlineKeyboardMarkup | None = None
