from __future__ import annotations

from typing import final

from .abc import TelegramMethod


@final
class ApproveChatJoinRequest(TelegramMethod[bool]):
    """See :meth:`yatbaf.bot.Bot.approve_chat_join_request`"""

    chat_id: str | int
    user_id: int
