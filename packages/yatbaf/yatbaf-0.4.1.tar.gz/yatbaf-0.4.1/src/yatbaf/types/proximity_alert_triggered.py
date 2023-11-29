from __future__ import annotations

from typing import final

from .abc import TelegramType
from .user import User


@final
class ProximityAlertTriggered(TelegramType):
    """This object represents the content of a service message, sent whenever
    a user in the chat triggers a proximity alert set by another user.

    See: https://core.telegram.org/bots/api#proximityalerttriggered
    """

    traveler: User
    """User that triggered the alert."""

    watcher: User
    """User that set the alert."""

    distance: int
    """The distance between the users."""
