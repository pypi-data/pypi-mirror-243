from __future__ import annotations

from typing import TYPE_CHECKING
from typing import final

from .abc import TelegramMethod

if TYPE_CHECKING:
    from yatbaf.types import ChatPermissions
    from yatbaf.typing import NoneBool


@final
class SetChatPermissions(TelegramMethod[bool]):
    """See :meth:`yatbaf.bot.Bot.set_chat_permissions`"""

    chat_id: str | int
    permissions: ChatPermissions
    use_independent_chat_permissions: NoneBool = None
