from __future__ import annotations

from typing import TYPE_CHECKING
from typing import final

from .abc import TelegramMethod

if TYPE_CHECKING:
    from yatbaf.typing import NoneBool
    from yatbaf.typing import NoneInt
    from yatbaf.typing import NoneStr


@final
class AnswerCallbackQuery(TelegramMethod[bool]):
    """See :meth:`yatbaf.bot.Bot.answer_callback_query()`"""

    callback_query_id: str
    text: NoneStr = None
    show_alert: NoneBool = None
    url: NoneStr = None
    cache_time: NoneInt = None
