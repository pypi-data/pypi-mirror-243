from typing import final

from .abc import TelegramType


@final
class GeneralForumTopicUnhidden(TelegramType):
    """This object represents a service message about General forum topic
    unhidden in the chat. Currently holds no information.

    See: https://core.telegram.org/bots/api#generalforumtopicunhidden
    """
