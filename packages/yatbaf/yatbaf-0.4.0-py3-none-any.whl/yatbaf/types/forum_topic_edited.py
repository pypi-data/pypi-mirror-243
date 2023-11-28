from __future__ import annotations

from typing import final

from yatbaf.typing import NoneStr

from .abc import TelegramType


@final
class ForumTopicEdited(TelegramType):
    """This object represents a service message about an edited forum topic.

    See: https://core.telegram.org/bots/api#forumtopicedited
    """

    name: NoneStr = None
    """*Optional.* New name of the topic, if it was edited."""

    icon_custom_emoji_id: NoneStr = None
    """*Optional.* New identifier of the custom emoji shown as the topic icon,
    if it was edited.

    .. note::

        An empty string if the icon was removed.
    """
