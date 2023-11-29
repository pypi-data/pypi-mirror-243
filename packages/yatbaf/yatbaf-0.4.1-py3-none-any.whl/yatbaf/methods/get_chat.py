from __future__ import annotations

from typing import final

from yatbaf.types import Chat

from .abc import TelegramMethod


@final
class GetChat(TelegramMethod[Chat]):
    """See :meth:`yatbaf.bot.Bot.get_chat`"""

    chat_id: str | int
