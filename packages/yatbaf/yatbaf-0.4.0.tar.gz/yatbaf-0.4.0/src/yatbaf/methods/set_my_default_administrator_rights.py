from __future__ import annotations

from typing import TYPE_CHECKING
from typing import final

from .abc import TelegramMethod

if TYPE_CHECKING:
    from yatbaf.types import ChatAdministratorRights
    from yatbaf.typing import NoneBool


@final
class SetMyDefaultAdministratorRights(TelegramMethod[bool]):
    """See :meth:`yatbaf.bot.Bot.set_my_default_administrator_rights`"""

    rights: ChatAdministratorRights | None = None
    for_channels: NoneBool = None
