from __future__ import annotations

from typing import TYPE_CHECKING
from typing import final

from yatbaf.types import BotDescription

from .abc import TelegramMethod

if TYPE_CHECKING:
    from yatbaf.typing import NoneStr


@final
class GetMyDescription(TelegramMethod[BotDescription]):
    """See :meth:`yatbaf.bot.Bot.get_my_description`"""

    language_code: NoneStr = None
