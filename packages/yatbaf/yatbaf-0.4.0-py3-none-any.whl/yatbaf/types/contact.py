from __future__ import annotations

from typing import final

from yatbaf.typing import NoneStr

from .abc import TelegramType


@final
class Contact(TelegramType):
    """This object represents a phone contact.

    See: https://core.telegram.org/bots/api#contact
    """

    phone_number: str
    """Contact's phone number."""

    first_name: str
    """Contact's first name."""

    last_name: NoneStr = None
    """*Optional.* Contact's last name."""

    user_id: NoneStr = None
    """*Optional.* Contact's user identifier in Telegram."""

    vcard: NoneStr = None
    """*Optional.* Additional data about the contact in the form of a vCard."""
