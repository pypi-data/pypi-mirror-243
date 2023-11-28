from __future__ import annotations

from typing import final

from yatbaf.typing import NoneInt
from yatbaf.typing import NoneStr

from .abc import TelegramType
from .location import Location


@final
class Venue(TelegramType):
    """This object represents a venue.

    See: https://core.telegram.org/bots/api#venue
    """

    location: Location
    """Venue location. Can't be a live location."""

    title: str
    """Name of the venue."""

    address: str
    """Address of the venue."""

    foursquare_id: NoneStr = None
    """*Optional.* Foursquare identifier of the venue."""

    foursquare_type: NoneStr = None
    """*Optional.* Foursquare type of the venue."""

    google_place_id: NoneInt = None
    """*Optional.* Google Places identifier of the venue."""

    google_place_type: NoneInt = None
    """*Optional.* Google Places type of the venue."""
