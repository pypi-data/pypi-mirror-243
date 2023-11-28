from __future__ import annotations

from typing import TYPE_CHECKING
from typing import final

from yatbaf.types import ChatAdministratorRights

from .abc import TelegramMethod

if TYPE_CHECKING:
    from yatbaf.typing import NoneBool


@final
class GetMyDefaultAdministratorRights(TelegramMethod[ChatAdministratorRights]):
    """See :meth:`yatbaf.bot.Bot.get_my_default_administrator_rights`"""

    for_channels: NoneBool = None
