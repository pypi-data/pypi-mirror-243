from __future__ import annotations

from typing import final

from .abc import TelegramMethod


@final
class CloseGeneralForumTopic(TelegramMethod[bool]):
    """See :meth:`yatbaf.bot.Bot.close_general_forum_topic`"""

    chat_id: str | int
