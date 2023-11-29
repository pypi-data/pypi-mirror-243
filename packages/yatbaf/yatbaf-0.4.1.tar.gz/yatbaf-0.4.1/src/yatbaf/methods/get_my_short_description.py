from __future__ import annotations

from typing import TYPE_CHECKING
from typing import final

from yatbaf.types import BotShortDescription

from .abc import TelegramMethod

if TYPE_CHECKING:
    from yatbaf.typing import NoneStr


@final
class GetMyShortDescription(TelegramMethod[BotShortDescription]):
    """See :meth:`yatbaf.bot.Bot.get_my_short_description`"""

    language_code: NoneStr = None
