from __future__ import annotations

from typing import final

from .abc import TelegramMethod


@final
class DeleteForumTopic(TelegramMethod[bool]):
    """See :meth:`yatbaf.bot.Bot.delete_forum_topic`"""

    chat_id: str | int
    message_thread_id: int
