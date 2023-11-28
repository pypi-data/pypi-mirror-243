from __future__ import annotations

from typing import final

from .abc import TelegramType
from .location import Location


@final
class ChatLocation(TelegramType):
    """Represents a location to which a chat is connected.

    See: https://core.telegram.org/bots/api#chatlocation
    """

    location: Location
    """The location to which the supergroup is connected.

    .. note::

        Can't be a live location.
    """

    address: str
    """Location address; 1-64 characters, as defined by the chat owner."""
