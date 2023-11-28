from __future__ import annotations

from typing import final

from .abc import TelegramType
from .labeled_price import LabeledPrice


@final
class ShippingOption(TelegramType):
    """This object represents one shipping option.

    See: https://core.telegram.org/bots/api#shippingoption
    """

    id: str
    """Shipping option identifier."""

    title: str
    """Option title."""

    prices: list[LabeledPrice]
    """List of price portions."""
