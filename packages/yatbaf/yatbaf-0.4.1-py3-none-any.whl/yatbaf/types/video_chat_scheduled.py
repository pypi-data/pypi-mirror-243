from __future__ import annotations

from typing import final

from .abc import TelegramType

# from datetime import datetime


@final
class VideoChatScheduled(TelegramType):
    """This object represents a service message about a video chat scheduled
    in the chat.

    See: https://core.telegram.org/bots/api#videochatscheduled
    """

    start_date: int  # datetime
    """Point in time (Unix timestamp) when the video chat is supposed to be
    started by a chat administrator.
    """
