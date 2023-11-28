from __future__ import annotations

from typing import TYPE_CHECKING
from typing import final

from .abc import TelegramMethod

if TYPE_CHECKING:
    from yatbaf.enums import ChatAction
    from yatbaf.typing import NoneInt


@final
class SendChatAction(TelegramMethod[bool]):
    """See :meth:`yatbaf.bot.Bot.send_chat_action`"""

    chat_id: str | int
    action: ChatAction
    message_thread_id: NoneInt = None
