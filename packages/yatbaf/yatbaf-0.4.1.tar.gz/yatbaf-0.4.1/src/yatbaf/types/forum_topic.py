from __future__ import annotations

from typing import final

from yatbaf.typing import NoneStr

from .abc import TelegramType


@final
class ForumTopic(TelegramType):
    """This object represents a forum topic.

    See: https://core.telegram.org/bots/api#forumtopic
    """

    message_thread_id: int
    """Unique identifier of the forum topic."""

    name: str
    """Name of the topic."""

    icon_color: int
    """Color of the topic icon in RGB format."""

    icon_custom_emoji_id: NoneStr = None
    """
    *Optional.* Unique identifier of the custom emoji shown as the topic icon.
    """
