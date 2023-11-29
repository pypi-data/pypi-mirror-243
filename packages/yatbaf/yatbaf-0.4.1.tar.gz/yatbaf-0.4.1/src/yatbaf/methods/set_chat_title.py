from __future__ import annotations

from typing import final

from .abc import TelegramMethod


@final
class SetChatTitle(TelegramMethod[bool]):
    """See :meth:`yatbaf.bot.Bot.set_chat_title`"""

    chat_id: str | int
    title: str
