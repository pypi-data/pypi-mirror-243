from __future__ import annotations

from typing import final

from .abc import TelegramMethod


@final
class UnpinAllChatMessages(TelegramMethod[bool]):
    """See :meth:`yatbaf.bot.Bot.unpin_all_chat_messages`"""

    chat_id: str | int
