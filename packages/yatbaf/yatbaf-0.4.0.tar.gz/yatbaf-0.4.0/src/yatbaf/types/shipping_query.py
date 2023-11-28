from __future__ import annotations

from typing import final

from msgspec import field

from .abc import TelegramType
from .shipping_address import ShippingAddress
from .user import User


@final
class ShippingQuery(TelegramType):
    """This object contains information about an incoming shipping query.

    See: https://core.telegram.org/bots/api#shippingquery
    """

    id: str
    """Unique query identifier."""

    from_: User = field(name="from")
    """User who sent the query."""

    invoice_payload: str
    """Bot specified invoice payload."""

    shipping_address: ShippingAddress
    """User specified shipping address."""
