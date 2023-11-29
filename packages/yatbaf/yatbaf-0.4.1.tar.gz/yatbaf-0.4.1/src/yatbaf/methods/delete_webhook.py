from __future__ import annotations

from typing import TYPE_CHECKING
from typing import final

from .abc import TelegramMethod

if TYPE_CHECKING:
    from yatbaf.typing import NoneBool


@final
class DeleteWebhook(TelegramMethod[bool]):
    """See :meth:`yatbaf.bot.Bot.selete_webhook`"""

    drop_pending_updates: NoneBool = None
