from __future__ import annotations

from typing import TYPE_CHECKING
from typing import final

from yatbaf.types import Message

from .abc import TelegramMethod

if TYPE_CHECKING:
    from yatbaf.types import InlineKeyboardMarkup
    from yatbaf.typing import NoneBool
    from yatbaf.typing import NoneInt


@final
class SendGame(TelegramMethod[Message]):
    """See :meth:`yatbaf.bot.Bot.send_game`"""

    chat_id: str | int
    game_short_name: str
    message_thread_id: NoneInt = None
    disable_notification: NoneBool = None
    protect_content: NoneBool = None
    reply_to_message_id: NoneInt = None
    allow_sending_without_reply: NoneBool = None
    reply_markup: InlineKeyboardMarkup | None = None
