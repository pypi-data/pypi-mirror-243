from __future__ import annotations

from typing import final

from yatbaf.enums import Currency

from .abc import TelegramType


@final
class Invoice(TelegramType):
    """This object contains basic information about an invoice.

    See: https://core.telegram.org/bots/api#invoice
    """

    title: str
    """Product name."""

    description: str
    """Product description."""

    start_parameter: str
    """
    Unique bot deep-linking parameter that can be used to generate this invoice.
    """

    currency: Currency
    """Three-letter ISO 4217 currency code."""

    total_amount: int
    """Total price in the smallest units of the currency.

    .. important::

        Integer, not float/double.
    """
