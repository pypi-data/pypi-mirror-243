from __future__ import annotations

from typing import final

from .abc import TelegramMethod


@final
class SetChatDescription(TelegramMethod[bool]):
    """See :meth:`yatbaf.bot.Bot.set_chat_description`"""

    chat_id: str | int
    description: str | None = None
