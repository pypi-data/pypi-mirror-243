from __future__ import annotations

from typing import final

from yatbaf.typing import NoneStr

from .abc import TelegramType


@final
class InputContactMessageContent(TelegramType):
    """Represents the content of a contact message to be sent as the result of
    an inline query.

    See: https://core.telegram.org/bots/api#inputcontactmessagecontent
    """

    phone_number: str
    """Contact's phone number."""

    first_name: str
    """Contact's first name."""

    last_name: NoneStr = None
    """*Optional.* Contact's last name."""

    vcard: NoneStr = None
    """*Optional.* Additional data about the contact in the form of a vCard,
    0-2048 bytes.
    """
