from __future__ import annotations

from typing import final

from yatbaf.typing import NoneStr

from .abc import TelegramType
from .order_info import OrderInfo


@final
class SuccessfulPayment(TelegramType, kw_only=True):
    """This object contains basic information about a successful payment.

    See: https://core.telegram.org/bots/api#successfulpayment
    """

    currency: str
    """Three-letter ISO 4217 currency code."""

    total_amount: int
    """Total price in the smallest units of the currency.

    .. important::

        Integer, not float/double.
    """

    invoice_payload: str
    """Bot specified invoice payload."""

    shipping_option_id: NoneStr = None
    """*Optional.* Identifier of the shipping option chosen by the user."""

    order_info: OrderInfo | None = None
    """*Optional.* Order information provided by the user."""

    telegram_payment_charge_id: str
    """Telegram payment identifier."""

    provider_payment_charge_id: str
    """Provider payment identifier."""
