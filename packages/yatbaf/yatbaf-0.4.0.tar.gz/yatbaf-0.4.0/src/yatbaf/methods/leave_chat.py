from __future__ import annotations

from typing import final

from .abc import TelegramMethod


@final
class LeaveChat(TelegramMethod[bool]):
    """See :meth:`yatbaf.bot.Bot.leave_chat`"""

    chat_id: str | int
