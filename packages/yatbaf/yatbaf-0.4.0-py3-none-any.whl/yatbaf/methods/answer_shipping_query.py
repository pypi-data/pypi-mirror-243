from __future__ import annotations

from typing import TYPE_CHECKING
from typing import final

from .abc import TelegramMethod

if TYPE_CHECKING:
    from yatbaf.types import ShippingOption
    from yatbaf.typing import NoneStr


@final
class AnswerShippingQuery(TelegramMethod[bool]):
    """See :meth:`yatbaf.bot.Bot.answer_shipping_query`"""

    shipping_query_id: str
    ok: bool
    shipping_options: list[ShippingOption] | None = None
    error_message: NoneStr = None
