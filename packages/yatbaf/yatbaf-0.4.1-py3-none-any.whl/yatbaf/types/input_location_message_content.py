from __future__ import annotations

from typing import final

from .abc import TelegramType


@final
class InputLocationMessageContent(TelegramType):
    """Represents the content of a location message to be sent as the result of
    an inline query.

    # https://core.telegram.org/bots/api#inputlocationmessagecontent
    """

    latitude: float
    """Latitude of the location in degrees."""

    longtitude: float
    """Longitude of the location in degrees."""

    horizontal_accuracy: float | None = None
    """*Optional.* The radius of uncertainty for the location, measured in
    meters; 0-1500.
    """

    live_period: int | None = None
    """*Optional.* Period in seconds for which the location can be updated,
    should be between 60 and 86400.
    """

    heading: int | None = None
    """*Optional.* For live locations, a direction in which the user is moving,
    in degrees. Must be between 1 and 360 if specified.
    """

    proximity_alert_radius: int | None = None
    """*Optional.* For live locations, a maximum distance for proximity alerts
    about approaching another chat member, in meters. Must be between 1 and
    100000 if specified.
    """
