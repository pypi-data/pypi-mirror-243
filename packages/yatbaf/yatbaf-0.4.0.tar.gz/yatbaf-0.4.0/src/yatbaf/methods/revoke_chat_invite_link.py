from __future__ import annotations

from typing import final

from yatbaf.types import ChatInviteLink

from .abc import TelegramMethod


@final
class RevokeChatInviteLink(TelegramMethod[ChatInviteLink]):
    """See :meth:`yatbaf.bot.Bot.revoke_chat_invite_link`"""

    chat_id: str | int
    invite_link: str
