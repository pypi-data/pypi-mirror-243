from typing import final

from .abc import TelegramType


@final
class ForumTopicReopened(TelegramType):
    """This object represents a service message about a forum topic reopened in
    the chat. Currently holds no information.

    See: https://core.telegram.org/bots/api#forumtopicreopened
    """
