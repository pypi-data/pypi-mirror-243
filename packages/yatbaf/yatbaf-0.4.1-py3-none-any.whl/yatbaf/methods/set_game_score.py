from __future__ import annotations

from typing import TYPE_CHECKING
from typing import final

from yatbaf.types import Message

from .abc import TelegramMethod

if TYPE_CHECKING:
    from yatbaf.typing import NoneBool
    from yatbaf.typing import NoneInt


@final
class SetGameScore(TelegramMethod[Message | bool]):
    """See :meth:`yatbaf.bot.Bot.set_game_score`"""

    user_id: int
    score: int
    force: NoneBool = None
    disable_edit_message: NoneBool = None
    chat_id: NoneInt = None
    message_id: NoneInt = None
    inline_message_id: NoneInt = None
