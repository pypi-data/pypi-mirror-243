from __future__ import annotations

from typing import final

from .abc import TelegramType


@final
class ChatShared(TelegramType):
    """This object contains information about the chat whose identifier was
    shared with the bot using a
    :class:`yatbaf.types.KeyboardButtonRequestChat` button.

    See: https://core.telegram.org/bots/api#chatshared
    """

    request_id: int
    """Identifier of the request."""

    chat_id: int
    """Identifier of the shared chat.

    .. note::

        The bot may not have access to the chat and could be unable to use
        this identifier, unless the chat is already known to the bot by some
        other means.
    """
