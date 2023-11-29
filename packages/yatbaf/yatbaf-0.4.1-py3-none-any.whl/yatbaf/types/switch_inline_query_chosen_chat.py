from __future__ import annotations

from typing import final

from yatbaf.typing import NoneBool
from yatbaf.typing import NoneStr

from .abc import TelegramType


@final
class SwitchInlineQueryChosenChat(TelegramType):
    """This object represents an inline button that switches the current user
    to inline mode in a chosen chat, with an optional default inline query.

    See: https://core.telegram.org/bots/api#switchinlinequerychosenchat
    """

    query: NoneStr = None
    """*Optional.* The default inline query to be inserted in the input field.
    If left empty, only the bot's username will be inserted.
    """

    allow_user_chats: NoneBool = None
    """*Optional.* ``True``, if private chats with users can be chosen."""

    allow_bot_chats: NoneBool = None
    """*Optional.* ``True``, if private chats with bots can be chosen."""

    allow_group_chats: NoneBool = None
    """*Optional.* ``True``, if group and supergroup chats can be chosen."""

    allow_channel_chats: NoneBool = None
    """*Optional.* ``True``, if channel chats can be chosen."""
