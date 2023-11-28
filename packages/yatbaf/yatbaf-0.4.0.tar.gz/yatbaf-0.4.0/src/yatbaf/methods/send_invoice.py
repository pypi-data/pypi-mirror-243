from __future__ import annotations

from typing import TYPE_CHECKING
from typing import final

from yatbaf.types import Message

from .abc import TelegramMethod

if TYPE_CHECKING:
    from yatbaf.types import InlineKeyboardMarkup
    from yatbaf.types import LabeledPrice
    from yatbaf.typing import NoneBool
    from yatbaf.typing import NoneInt
    from yatbaf.typing import NoneStr


@final
class SendInvoice(TelegramMethod[Message]):
    """See :meth:`yatbaf.bot.Bot.send_invoice`"""

    chat_id: str | int
    title: str
    description: str
    payload: str
    provider_token: str
    currency: str
    prices: list[LabeledPrice]
    message_thread_id: NoneInt = None
    max_tip_amount: NoneInt = None
    suggested_tip_amounts: list[int] | None = None
    start_parameter: NoneStr = None
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
    disable_notification: NoneBool = None
    protect_content: NoneBool = None
    reply_to_message_id: NoneInt = None
    allow_sending_without_reply: NoneBool = None
    reply_markup: InlineKeyboardMarkup | None = None
