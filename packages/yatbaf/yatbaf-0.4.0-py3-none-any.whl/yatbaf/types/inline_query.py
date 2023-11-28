from __future__ import annotations

from typing import final

from msgspec import field

from yatbaf.enums import ChatType

from .abc import TelegramType
from .location import Location
from .user import User


@final
class InlineQuery(TelegramType):
    """This object represents an incoming inline query. When the user sends an
    empty query, your bot could return some default or trending results.

    See: https://core.telegram.org/bots/api#inlinequery
    """

    id: str
    """Unique identifier for this query."""

    from_: User = field(name="from")
    """Sender"""

    query: str
    """Text of the query (up to 256 characters)"""

    offset: str
    """Offset of the results to be returned, can be controlled by the bot"""

    chat_type: ChatType | None = None
    """*Optional.* Type of the chat from which the inline query was sent.

    .. note::

        The chat type should be always known for requests sent from official
        clients and most third-party clients, unless the request was sent from
        a secret chat.
    """

    location: Location | None = None
    """*Optional.* Sender location, only for bots that request user location."""
