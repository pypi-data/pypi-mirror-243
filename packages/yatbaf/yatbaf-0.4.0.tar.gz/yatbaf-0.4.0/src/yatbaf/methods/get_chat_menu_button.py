from __future__ import annotations

from typing import final

from yatbaf.types import MenuButton

from .abc import TelegramMethod


@final
class GetChatMenuButton(TelegramMethod[MenuButton]):
    """See :meth:`yatbaf.bot.Bot.get_chat_menu_button`"""

    chat_id: str | int
