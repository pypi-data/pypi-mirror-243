from __future__ import annotations

from typing import TYPE_CHECKING
from typing import final

from .abc import TelegramMethod

if TYPE_CHECKING:
    from yatbaf.typing import NoneBool


@final
class UnbanChatMember(TelegramMethod[bool]):
    """See :meth:`yatbaf.bot.Bot.unban_chat_member`"""

    chat_id: str | int
    user_id: str | int
    only_if_banned: NoneBool = None
