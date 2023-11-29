from __future__ import annotations

from typing import final

from yatbaf.types import ChatMember

from .abc import TelegramMethod


@final
class GetChatAdministrators(TelegramMethod[list[ChatMember]]):
    """See :meth:`yatbaf.bot.Bot.get_chat_administrators`"""

    chat_id: str | int
