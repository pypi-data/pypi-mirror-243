from __future__ import annotations

from typing import final

from .abc import TelegramType


@final
class MessageId(TelegramType):
    """This object represents a unique message identifier.

    See: https://core.telegram.org/bots/api#messageid
    """

    message_id: int
    """Unique message identifier."""
