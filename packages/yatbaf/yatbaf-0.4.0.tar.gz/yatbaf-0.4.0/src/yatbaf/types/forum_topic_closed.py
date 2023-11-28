from __future__ import annotations

from typing import final

from .abc import TelegramType


@final
class ForumTopicClosed(TelegramType):
    """This object represents a service message about a forum topic closed in
    the chat. Currently holds no information.

    See: https://core.telegram.org/bots/api#forumtopicclosed
    """
