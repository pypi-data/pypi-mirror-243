from __future__ import annotations

from typing import TYPE_CHECKING
from typing import final

from yatbaf.types import ChatInviteLink

from .abc import TelegramMethod

if TYPE_CHECKING:
    from yatbaf.typing import NoneBool
    from yatbaf.typing import NoneInt
    from yatbaf.typing import NoneStr


@final
class EditChatInviteLink(TelegramMethod[ChatInviteLink]):
    """See :meth:`yatbaf.bot.Bot.edit_chat_invite_link`"""

    chat_id: str | int
    invite_link: str
    name: NoneStr = None
    expire_date: NoneInt = None
    member_limit: NoneInt = None
    creates_join_request: NoneBool = None
