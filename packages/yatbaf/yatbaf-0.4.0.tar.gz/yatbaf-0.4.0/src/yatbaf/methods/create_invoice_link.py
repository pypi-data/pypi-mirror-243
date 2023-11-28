from __future__ import annotations

from typing import TYPE_CHECKING
from typing import final

from .abc import TelegramMethod

if TYPE_CHECKING:
    from yatbaf.types import LabeledPrice
    from yatbaf.typing import NoneBool
    from yatbaf.typing import NoneInt
    from yatbaf.typing import NoneStr


@final
class CreateInvoiceLink(TelegramMethod[str]):
    """See :meth:`yatbaf.bot.Bot.create_invoice_link`"""

    title: str
    description: str
    payload: str
    provider_token: str
    currency: str
    prices: list[LabeledPrice]
    max_tip_amount: NoneInt = None
    suggested_tip_amounts: list[int] | None = None
    provider_data: NoneStr = None
    photo_url: str | None = None
    photo_size: NoneInt = None
    photo_width: NoneInt = None
    photo_height: NoneInt = None
    need_name: NoneBool = None
    need_phone_number: NoneBool = None
    need_email: NoneBool = None
    need_shipping_address: NoneBool = None
    send_phone_number_to_provider: NoneBool = None
    send_email_to_provider: NoneBool = None
    is_flexible: NoneBool = None
