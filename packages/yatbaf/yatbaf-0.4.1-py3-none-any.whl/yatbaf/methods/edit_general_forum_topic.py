from __future__ import annotations

from typing import final

from .abc import TelegramMethod


@final
class EditGeneralForumTopic(TelegramMethod[bool]):
    """See :meth:`yatbaf.bot.Bot.edit_general_forum_topic`"""

    chat_id: str | int
    name: str
