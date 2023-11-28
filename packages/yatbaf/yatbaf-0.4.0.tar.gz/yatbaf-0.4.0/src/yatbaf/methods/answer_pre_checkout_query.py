from __future__ import annotations

from typing import TYPE_CHECKING
from typing import final

from .abc import TelegramMethod

if TYPE_CHECKING:
    from yatbaf.typing import NoneStr


@final
class AnswerPreCheckoutQuery(TelegramMethod[bool]):
    """See :meth:`yatbaf.bot.Bot.answer_pre_checkout_query`"""

    pre_checkout_query_id: str
    ok: bool
    error_message: NoneStr = None
