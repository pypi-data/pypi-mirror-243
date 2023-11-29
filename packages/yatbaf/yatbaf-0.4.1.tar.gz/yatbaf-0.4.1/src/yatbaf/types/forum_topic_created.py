from __future__ import annotations

from typing import final

from yatbaf.typing import NoneStr

from .abc import TelegramType


@final
class ForumTopicCreated(TelegramType):
    """This object represents a service message about a new forum topic created
    in the chat.

    See: https://core.telegram.org/bots/api#forumtopiccreated
    """

    name: str
    """Name of the topic."""

    icon_color: int
    """Color of the topic icon in RGB format."""

    icon_custom_emoji_id: NoneStr = None
    """*Optional.* Unique identifier of the custom emoji shown as the topic icon."""  # noqa: E501
