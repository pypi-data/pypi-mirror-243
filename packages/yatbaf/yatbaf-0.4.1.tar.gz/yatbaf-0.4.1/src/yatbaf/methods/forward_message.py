from __future__ import annotations

from typing import TYPE_CHECKING
from typing import final

from yatbaf.types import Message

from .abc import TelegramMethod

if TYPE_CHECKING:
    from yatbaf.typing import NoneBool
    from yatbaf.typing import NoneInt


@final
class ForwardMessage(TelegramMethod[Message]):
    """See :meth:`yatbaf.bot.Bot.forward_message`"""

    chat_id: str | int
    from_chat_id: int | str
    message_id: int
    message_thread_id: NoneInt = None
    disable_notification: NoneBool = None
    protect_content: NoneBool = None
