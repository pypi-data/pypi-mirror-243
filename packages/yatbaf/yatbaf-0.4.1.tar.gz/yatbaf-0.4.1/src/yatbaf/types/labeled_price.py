from __future__ import annotations

from typing import final

from .abc import TelegramType


@final
class LabeledPrice(TelegramType):
    """This object represents a portion of the price for goods or services.

    See: https://core.telegram.org/bots/api#labeledprice
    """

    label: str
    """Portion label."""

    amount: int
    """Price of the product in the smallest units of the currency.

    .. important::

        Integer, not float/double.
    """
