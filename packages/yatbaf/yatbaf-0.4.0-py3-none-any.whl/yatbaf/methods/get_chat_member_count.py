from __future__ import annotations

from typing import final

from .abc import TelegramMethod


@final
class GetChatMemberCount(TelegramMethod[int]):
    """See :meth:`yatbaf.bot.Bot.get_chat_member_count`"""

    chat_id: str | int
