from __future__ import annotations

from typing import TYPE_CHECKING
from typing import final

from .abc import TelegramMethod

if TYPE_CHECKING:
    from yatbaf.typing import NoneStr


@final
class SetMyShortDescription(TelegramMethod[bool]):
    """See :meth:`yatbaf.bot.Bot.set_my_short_description`"""

    short_description: NoneStr = None
    language_code: NoneStr = None
