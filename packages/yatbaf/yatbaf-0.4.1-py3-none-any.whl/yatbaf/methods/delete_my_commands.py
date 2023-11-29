from __future__ import annotations

from typing import TYPE_CHECKING
from typing import final

from .abc import TelegramMethod

if TYPE_CHECKING:
    from yatbaf.types import BotCommandScope
    from yatbaf.typing import NoneStr


@final
class DeleteMyCommands(TelegramMethod[bool]):
    """See :meth:`yatbaf.bot.Bot.delete_my_commands`"""

    scope: BotCommandScope | None = None
    language_code: NoneStr = None
