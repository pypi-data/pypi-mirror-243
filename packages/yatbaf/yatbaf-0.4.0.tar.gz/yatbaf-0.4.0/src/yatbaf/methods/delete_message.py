from __future__ import annotations

from typing import final

from .abc import TelegramMethod


@final
class DeleteMessage(TelegramMethod[bool]):
    """See :meth:`yatbaf.bot.Bot.delete_message`"""

    chat_id: str | int
    message_id: int
