from __future__ import annotations

from typing import TYPE_CHECKING
from typing import final

from yatbaf.types import ForumTopic

from .abc import TelegramMethod

if TYPE_CHECKING:
    from yatbaf.enums import IconColor
    from yatbaf.typing import NoneStr


@final
class CreateForumTopic(TelegramMethod[ForumTopic]):
    """See :meth:`yatbaf.bot.Bot.create_forum_topic`"""

    chat_id: str | int
    name: str
    icon_color: IconColor | None = None
    icon_custom_emoji_id: NoneStr = None
