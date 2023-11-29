from __future__ import annotations

from typing import TYPE_CHECKING
from typing import final

from yatbaf.types import GameHighScore

from .abc import TelegramMethod

if TYPE_CHECKING:
    from yatbaf.typing import NoneInt
    from yatbaf.typing import NoneStr


@final
class GetGameHighScores(TelegramMethod[list[GameHighScore]]):
    """See :meth:`yatbaf.bot.Bot.get_game_high_scores`"""

    user_id: int
    chat_id: NoneInt = None
    message_id: NoneInt = None
    inline_message_id: NoneStr = None
