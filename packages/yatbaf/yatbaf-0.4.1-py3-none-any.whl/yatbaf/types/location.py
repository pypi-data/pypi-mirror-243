from __future__ import annotations

from typing import final

from yatbaf.typing import NoneInt

from .abc import TelegramType


@final
class Location(TelegramType):
    """This object represents a point on the map.

    See: https://core.telegram.org/bots/api#location
    """

    longtitude: float
    """Longitude as defined by sender."""

    latitude: float
    """Latitude as defined by sender."""

    horizontal_accuracy: float | None = None
    """*Optional.* The radius of uncertainty for the location, measured in
    meters; 0-1500.
    """

    live_period: NoneInt = None
    """*Optional.* Time relative to the message sending date, during which the
    location can be updated; in seconds.

    .. note::

        For active live locations only.
    """

    heading: NoneInt = None
    """*Optional.* The direction in which user is moving, in degrees; 1-360.

    .. note::

        For active live locations only.
    """

    proximity_alert_radius: NoneInt = None
    """*Optional.* The maximum distance for proximity alerts about approaching
    another chat member, in meters.

    .. note::

        For sent live locations only.
    """
