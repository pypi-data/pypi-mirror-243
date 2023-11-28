from __future__ import annotations

from typing import final

from .abc import TelegramMethod


@final
class HideGeneralForumTopic(TelegramMethod[bool]):
    """See :meth:`yatbaf.bot.Bot.hide_general_forum_topic`"""

    chat_id: str | int
