from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import final

from .abc import TelegramMethodWithFile

if TYPE_CHECKING:
    from yatbaf.enums import UpdateType
    from yatbaf.typing import InputFile
    from yatbaf.typing import NoneBool
    from yatbaf.typing import NoneStr


@final
class SetWebhook(TelegramMethodWithFile[bool]):
    """See :meth:`yatbaf.bot.Bot.set_webhook`"""

    url: str
    certificate: InputFile | None = None
    ip_address: NoneStr = None
    max_connections: int | None = None
    allowed_updates: list[UpdateType] | None = None
    drop_pending_updates: NoneBool = None
    secret_token: str | None = None

    __meth_file_fields__: ClassVar[tuple[str, ...]] = ("certificate",)
