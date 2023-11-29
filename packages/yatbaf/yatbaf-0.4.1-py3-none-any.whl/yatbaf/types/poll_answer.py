from __future__ import annotations

from typing import final

from .abc import TelegramType
from .chat import Chat
from .user import User


@final
class PollAnswer(TelegramType):
    """This object represents an answer of a user in a non-anonymous poll.

    See: https://core.telegram.org/bots/api#pollanswer
    """

    poll_id: str
    """Unique poll identifier."""

    option_ids: list[int]
    """0-based identifiers of answer options, chosen by the user. May be empty
    if the user retracted their vote.
    """

    voter_chat: Chat | None = None
    """*Optional.* The chat that changed the answer to the poll, if the voter
    is anonymous.
    """

    user: User | None = None
    """*Optional.* The user that changed the answer to the poll, if the voter
    isn't anonymous.
    """
