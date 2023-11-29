from __future__ import annotations

from typing import TYPE_CHECKING
from typing import final

from .abc import TelegramMethod

if TYPE_CHECKING:
    from yatbaf.types import PassportElementError


@final
class SetPassportDataErrors(TelegramMethod[bool]):
    """See :meth:`yatbaf.bot.Bot.set_passport_data_errors`"""

    user_id: int
    errors: list[PassportElementError]
