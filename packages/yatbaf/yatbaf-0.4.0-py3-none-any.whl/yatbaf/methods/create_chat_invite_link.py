from __future__ import annotations

from typing import TYPE_CHECKING
from typing import final

from yatbaf.types import ChatInviteLink

from .abc import TelegramMethod

if TYPE_CHECKING:
    from yatbaf.typing import NoneBool
    from yatbaf.typing import NoneInt
    from yatbaf.typing import NoneStr

# from datetime import timedelta


@final
class CreateChatInviteLink(TelegramMethod[ChatInviteLink]):
    """See :meth:`yatbaf.bot.Bot.create_chat_invite_link`"""

    chat_id: str | int
    name: NoneStr = None
    expire_date: int | None = None  # TODO: timedelta
    member_limit: NoneInt = None
    creates_join_request: NoneBool = None
