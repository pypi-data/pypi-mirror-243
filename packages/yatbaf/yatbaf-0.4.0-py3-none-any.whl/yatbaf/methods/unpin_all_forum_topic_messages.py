from __future__ import annotations

from typing import final

from .abc import TelegramMethod


@final
class UnpinAllForumTopicMessages(TelegramMethod[bool]):
    """See :meth:`yatbaf.bot.Bot.unpin_all_forum_topic_messages`"""

    chat_id: str | int
    message_thread_id: int
