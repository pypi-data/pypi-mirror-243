from __future__ import annotations

from typing import final

from .abc import TelegramType


@final
class UserShared(TelegramType):
    """This object contains information about the user whose identifier was
    shared with the bot using a :class:`KeyboardButtonRequestUser <yatbaf.types.keyboard_button.KeyboardButtonRequestUser>` button.

    See: https://core.telegram.org/bots/api#usershared
    """  # noqa: E501

    request_id: int
    """Identifier of the request."""

    user_id: int
    """Identifier of the shared user."""
