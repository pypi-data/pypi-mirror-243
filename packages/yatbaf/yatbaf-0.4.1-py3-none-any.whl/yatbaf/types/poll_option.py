from __future__ import annotations

from typing import final

from .abc import TelegramType


@final
class PollOption(TelegramType):
    """This object contains information about one answer option in a poll.

    See: https://core.telegram.org/bots/api#polloption
    """

    text: str
    """Option text, 1-100 characters."""

    vote_count: int
    """Number of users that voted for this option."""
