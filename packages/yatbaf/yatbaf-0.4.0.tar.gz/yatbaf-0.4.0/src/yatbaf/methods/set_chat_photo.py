from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import final

from .abc import TelegramMethodWithFile

if TYPE_CHECKING:
    from yatbaf.typing import InputFile


@final
class SetChatPhoto(TelegramMethodWithFile[bool]):
    """See :meth:`yatbaf.bot.Bot.set_chat_photo`"""

    chat_id: str | int
    photo: InputFile

    __meth_file_fields__: ClassVar[tuple[str, ...]] = ("photo",)
