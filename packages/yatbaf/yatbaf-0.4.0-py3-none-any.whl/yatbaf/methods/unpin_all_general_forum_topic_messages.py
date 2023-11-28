from __future__ import annotations

from typing import final

from .abc import TelegramMethod


@final
class UnpinAllGeneralForumTopicMessages(TelegramMethod[bool]):
    """See :meth:`yatbaf.bot.Bot.unpin_all_general_forum_topic_messages"""

    chat_id: str | int
