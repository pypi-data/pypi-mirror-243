from __future__ import annotations

from typing import final

from .abc import TelegramMethod


@final
class CloseForumTopic(TelegramMethod[bool]):
    """See :meth:`yatbaf.bot.Bot.close_forum_topic`"""

    chat_id: str | int
    message_thread_id: int
