from __future__ import annotations

from typing import final

from .abc import TelegramType


@final
class VideoChatEnded(TelegramType):
    """This object represents a service message about a video chat ended in
    the chat.

    See: https://core.telegram.org/bots/api#videochatended
    """

    duration: int
    """Video chat duration in seconds."""
