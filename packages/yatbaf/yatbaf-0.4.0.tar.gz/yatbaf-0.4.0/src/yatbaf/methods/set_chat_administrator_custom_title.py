from __future__ import annotations

from typing import final

from .abc import TelegramMethod


@final
class SetChatAdministratorCustomTitle(TelegramMethod[bool]):
    """See :meth:`yatbaf.bot.Bot.set_chat_administrator_custom_title`"""

    chat_id: str | int
    user_id: int
    custom_title: str
