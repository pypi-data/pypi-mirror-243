from __future__ import annotations

from typing import TYPE_CHECKING
from typing import final

from .abc import TelegramMethod

if TYPE_CHECKING:
    from yatbaf.types import BotCommand
    from yatbaf.types import BotCommandScope
    from yatbaf.typing import NoneStr


@final
class SetMyCommands(TelegramMethod[bool]):
    """See :meth:`yatbaf.bot.Bot.set_my_commands`"""

    commands: list[BotCommand]
    scope: BotCommandScope | None = None
    language_code: NoneStr = None
