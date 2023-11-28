from typing import final

from .abc import TelegramType


@final
class Story(TelegramType):
    """This object represents a message about a forwarded story in the chat.
    Currently holds no information.

    See: https://core.telegram.org/bots/api#story
    """
