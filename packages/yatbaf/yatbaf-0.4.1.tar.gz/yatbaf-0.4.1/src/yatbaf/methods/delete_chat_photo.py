from __future__ import annotations

from typing import final

from .abc import TelegramMethod


@final
class DeleteChatPhoto(TelegramMethod[bool]):
    """See :meth:`yatbaf.bot.Bot.delete_chat_photo`"""

    chat_id: str | int
