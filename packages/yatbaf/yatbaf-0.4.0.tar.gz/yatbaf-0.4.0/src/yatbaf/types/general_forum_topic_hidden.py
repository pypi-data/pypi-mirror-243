from typing import final

from .abc import TelegramType


@final
class GeneralForumTopicHidden(TelegramType):
    """This object represents a service message about General forum topic
    hidden in the chat. Currently holds no information.

    See: https://core.telegram.org/bots/api#generalforumtopichidden
    """
