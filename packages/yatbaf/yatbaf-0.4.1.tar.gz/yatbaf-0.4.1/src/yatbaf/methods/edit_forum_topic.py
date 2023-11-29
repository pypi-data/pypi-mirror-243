from __future__ import annotations

from typing import TYPE_CHECKING
from typing import final

from .abc import TelegramMethod

if TYPE_CHECKING:
    from yatbaf.typing import NoneStr


@final
class EditForumTopic(TelegramMethod[bool]):
    """See :meth:`yatbaf.bot.Bot.edit_forum_topic`"""

    chat_id: str | int
    message_thread_id: int
    name: NoneStr = None
    icon_custom_emoji_id: NoneStr = None
