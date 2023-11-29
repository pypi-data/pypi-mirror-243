from __future__ import annotations

from typing import final

from .abc import TelegramType
from .user import User


@final
class VideoChatParticipantsInvited(TelegramType):
    """This object represents a service message about new members invited to a
    video chat.

    See: https://core.telegram.org/bots/api#videochatparticipantsinvited
    """

    users: list[User]
    """New members that were invited to the video chat."""
