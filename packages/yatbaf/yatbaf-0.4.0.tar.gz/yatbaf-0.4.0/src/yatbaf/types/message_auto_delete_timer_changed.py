from __future__ import annotations

from typing import final

from .abc import TelegramType


@final
class MessageAutoDeleteTimerChanged(TelegramType):
    """This object represents a service message about a change in auto-delete
    timer settings.

    See: https://core.telegram.org/bots/api#messageautodeletetimerchanged
    """

    message_auto_delete_time: int
    """New auto-delete time for messages in the chat; in seconds."""
