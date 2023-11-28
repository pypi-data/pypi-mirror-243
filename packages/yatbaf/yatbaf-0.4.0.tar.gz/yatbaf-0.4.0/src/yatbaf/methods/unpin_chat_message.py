from __future__ import annotations

from typing import final

from .abc import TelegramMethod


@final
class UnpinChatMessage(TelegramMethod[bool]):
    """See :meth:`yatbaf.bot.Bot.unpin_chat_message`"""

    chat_id: str | int
    message_id: int | None = None
