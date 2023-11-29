from __future__ import annotations

from typing import TYPE_CHECKING
from typing import final

from yatbaf.types import Message

from .abc import TelegramMethod

if TYPE_CHECKING:
    from yatbaf.types import InlineKeyboardMarkup
    from yatbaf.typing import NoneInt
    from yatbaf.typing import NoneStr


@final
class StopMessageLiveLocation(TelegramMethod[Message | bool]):
    """See :meth:`yatbaf.bot.Bot.stop_message_live_location`"""

    chat_id: str | int | None = None
    message_id: NoneInt = None
    inline_message_id: NoneStr = None
    reply_markup: InlineKeyboardMarkup | None = None
