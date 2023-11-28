from __future__ import annotations

from typing import TYPE_CHECKING
from typing import final

from .abc import TelegramMethod

if TYPE_CHECKING:
    from yatbaf.types import InlineQueryResult
    from yatbaf.types import InlineQueryResultsButton
    from yatbaf.typing import NoneBool
    from yatbaf.typing import NoneInt
    from yatbaf.typing import NoneStr


@final
class AnswerInlineQuery(TelegramMethod[bool]):
    """See :meth:`yatbaf.bot.Bot.answer_inline_query`"""

    inline_query_id: str
    results: list[InlineQueryResult]
    cache_time: NoneInt = None
    is_personal: NoneBool = None
    next_offset: NoneStr = None
    button: InlineQueryResultsButton | None = None
