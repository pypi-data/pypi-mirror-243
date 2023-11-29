from __future__ import annotations

from typing import TYPE_CHECKING
from typing import final

from .abc import TelegramMethod

if TYPE_CHECKING:
    from yatbaf.types import ChatPermissions
    from yatbaf.typing import NoneBool

# from datetime import timedelta


@final
class RestrictChatMember(TelegramMethod[bool]):
    """See :meth:`yatbaf.bot.Bot.restrict_chat_member`"""

    chat_id: str | int
    user_id: str | int
    permissions: ChatPermissions
    use_independent_chat_permissions: NoneBool = None
    until_date: int | None = None  # timedelta
