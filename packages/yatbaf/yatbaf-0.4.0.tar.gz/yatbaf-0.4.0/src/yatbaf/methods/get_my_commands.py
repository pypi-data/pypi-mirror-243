from __future__ import annotations

from typing import TYPE_CHECKING
from typing import final

from yatbaf.types import BotCommand

from .abc import TelegramMethod

if TYPE_CHECKING:
    from yatbaf.types import BotCommandScope
    from yatbaf.typing import NoneStr


@final
class GetMyCommands(TelegramMethod[list[BotCommand]]):
    """See :meth:`yatbaf.bot.Bot.get_my_commands`"""

    scope: BotCommandScope | None = None
    language_code: NoneStr = None
