from __future__ import annotations

from typing import final

from msgspec import field

from yatbaf.typing import NoneStr

from .abc import TelegramType
from .order_info import OrderInfo
from .user import User


@final
class PreCheckoutQuery(TelegramType):
    """This object contains information about an incoming pre-checkout query.

    See: https://core.telegram.org/bots/api#precheckoutquery
    """

    id: str
    """Unique query identifier."""

    from_: User = field(name="from")
    """User who sent the query."""

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

    async def answer(self, ok: bool, error_message: NoneStr = None) -> bool:
        """See: :meth:`answer_pre_checkout_query <yatbaf.bot.Bot.answer_pre_checkout_query>`"""  # noqa: E501

        return await self.bot.answer_pre_checkout_query(
            pre_checkout_query_id=self.id,
            ok=ok,
            error_message=error_message,
        )
