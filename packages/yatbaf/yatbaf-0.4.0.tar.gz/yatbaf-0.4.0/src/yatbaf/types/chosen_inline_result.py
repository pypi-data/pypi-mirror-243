from __future__ import annotations

from typing import final

from msgspec import field

from yatbaf.typing import NoneStr

from .abc import TelegramType
from .location import Location
from .user import User


@final
class ChosenInlineResult(TelegramType):
    """Represents a result of an inline query that was chosen by the user and
    sent to their chat partner.

    See: https://core.telegram.org/bots/api#choseninlineresult
    """

    result_id: int
    """The unique identifier for the result that was chosen."""

    from_: User = field(name="from")
    """The user that chose the result."""

    query: str
    """The query that was used to obtain the result."""

    location: Location | None = None
    """*Optional.* Sender location, only for bots that require user location."""

    inline_message_id: NoneStr = None
    """*Optional.* Identifier of the sent inline message. Available only if
    there is an inline keyboard attached to the message. Will be also received
    in callback queries and can be used to edit the message.
    """
