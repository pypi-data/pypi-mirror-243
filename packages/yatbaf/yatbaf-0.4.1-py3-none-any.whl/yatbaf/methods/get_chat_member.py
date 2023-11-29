from __future__ import annotations

from typing import final

from yatbaf.types import ChatMember

from .abc import TelegramMethod


@final
class GetChatMember(TelegramMethod[ChatMember]):
    """See :meth:`yatbaf.bot.Bot.get_chat_member`"""

    chat_id: str | int
    user_id: int
