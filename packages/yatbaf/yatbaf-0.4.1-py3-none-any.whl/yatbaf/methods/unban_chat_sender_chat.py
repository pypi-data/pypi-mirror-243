from __future__ import annotations

from typing import final

from .abc import TelegramMethod


@final
class UnbanChatSenderChat(TelegramMethod[bool]):
    """See :meth:`yatbaf.bot.Bot.unban_chat_sender_chat`"""

    chat_id: str | int
    sender_chat_id: int
