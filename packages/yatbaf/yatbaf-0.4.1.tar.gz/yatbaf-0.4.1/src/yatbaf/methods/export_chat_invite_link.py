from __future__ import annotations

from typing import final

from .abc import TelegramMethod


@final
class ExportChatInviteLink(TelegramMethod[str]):
    """See :meth:`yatbaf.bot.Bot.export_chat_invite_link`"""

    chat_id: str | int
