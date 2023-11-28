from __future__ import annotations

from typing import TYPE_CHECKING
from typing import final

from .abc import TelegramMethod

if TYPE_CHECKING:
    from yatbaf.types import MenuButton


@final
class SetChatMenuButton(TelegramMethod[bool]):
    """See :meth:`yatbaf.bot.Bot.set_chat_menu_button`"""

    chat_id: str | int | None = None
    menu_button: MenuButton | None = None
