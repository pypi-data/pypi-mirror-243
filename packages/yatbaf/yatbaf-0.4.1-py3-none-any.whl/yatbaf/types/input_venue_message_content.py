from __future__ import annotations

from typing import final

from yatbaf.typing import NoneStr

from .abc import TelegramType


@final
class InputVenueMessageContent(TelegramType):
    """Represents the content of a venue message to be sent as the result of an
    inline query.

    See: https://core.telegram.org/bots/api#inputvenuemessagecontent
    """

    latitude: float
    """Latitude of the venue in degrees."""

    longtitude: float
    """Longitude of the venue in degrees."""

    title: str
    """Name of the venue."""

    address: str
    """Address of the venue."""

    foursquare_id: NoneStr = None
    """*Optional.* Foursquare identifier of the venue, if known."""

    foursquare_type: NoneStr = None
    """*Optional.* Foursquare type of the venue, if known. (For example,
    “arts_entertainment/default”, “arts_entertainment/aquarium” or
    “food/icecream”.)
    """

    google_place_id: NoneStr = None
    """*Optional.* Google Places identifier of the venue."""

    google_place_type: NoneStr = None
    """*Optional.* Google Places type of the venue."""
