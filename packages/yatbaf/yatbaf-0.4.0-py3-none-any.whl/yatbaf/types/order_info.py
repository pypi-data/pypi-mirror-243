from __future__ import annotations

from typing import final

from yatbaf.typing import NoneStr

from .abc import TelegramType
from .shipping_address import ShippingAddress


@final
class OrderInfo(TelegramType):
    """This object represents information about an order.

    See: https://core.telegram.org/bots/api#orderinfo
    """

    name: NoneStr = None
    """*Optional.* User name."""

    phone_number: NoneStr = None
    """*Optional.* User's phone number."""

    email: NoneStr = None
    """*Optional.* User email."""

    shipping_address: ShippingAddress | None = None
    """*Optional.* User shipping address."""
