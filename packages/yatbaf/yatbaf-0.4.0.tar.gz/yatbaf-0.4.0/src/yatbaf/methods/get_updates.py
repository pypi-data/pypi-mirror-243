from __future__ import annotations

from typing import TYPE_CHECKING
from typing import final

from yatbaf.enums import UpdateType
from yatbaf.types import Update

from .abc import TelegramMethod

if TYPE_CHECKING:
    from yatbaf.typing import NoneInt


@final
class GetUpdates(TelegramMethod[list[Update]]):
    """See :meth:`yatbaf.bot.Bot.get_updates`"""

    offset: NoneInt = None
    limit: NoneInt = None
    timeout: float | None = None
    allowed_updates: list[UpdateType] | None = None
