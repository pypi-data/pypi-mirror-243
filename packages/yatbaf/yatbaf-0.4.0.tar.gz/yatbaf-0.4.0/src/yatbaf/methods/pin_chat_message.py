from __future__ import annotations

from typing import TYPE_CHECKING
from typing import final

from .abc import TelegramMethod

if TYPE_CHECKING:
    from yatbaf.typing import NoneBool


@final
class PinChatMessage(TelegramMethod[bool]):
    """See :meth:`yatbaf.bot.Bot.pin_chat_message`"""

    chat_id: str | int
    message_id: int
    disable_notification: NoneBool = None
