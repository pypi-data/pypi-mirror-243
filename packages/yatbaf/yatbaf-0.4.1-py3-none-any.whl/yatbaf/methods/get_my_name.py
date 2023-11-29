from __future__ import annotations

from typing import TYPE_CHECKING
from typing import final

from yatbaf.types import BotName

from .abc import TelegramMethod

if TYPE_CHECKING:
    from yatbaf.typing import NoneStr


@final
class GetMyName(TelegramMethod[BotName]):
    """See :meth:`yatbaf.bot.Bot.get_my_name`"""

    language_code: NoneStr = None
