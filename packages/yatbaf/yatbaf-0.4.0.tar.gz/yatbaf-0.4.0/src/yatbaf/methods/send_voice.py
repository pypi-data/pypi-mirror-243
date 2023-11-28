from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import final

from yatbaf.types import Message

from .abc import TelegramMethodWithFile

if TYPE_CHECKING:
    from yatbaf.enums import ParseMode
    from yatbaf.types import MessageEntity
    from yatbaf.typing import InputFile
    from yatbaf.typing import NoneBool
    from yatbaf.typing import NoneInt
    from yatbaf.typing import NoneStr
    from yatbaf.typing import ReplyMarkup


@final
class SendVoice(TelegramMethodWithFile[Message]):
    """See :meth:`yatbaf.bot.Bot.send_voice`"""

    chat_id: str | int
    voice: InputFile | str
    message_thread_id: NoneInt = None
    caption: NoneStr = None
    parse_mode: ParseMode | None = None
    caption_entities: list[MessageEntity] | None = None
    duration: NoneInt = None
    disable_notification: NoneBool = None
    protect_content: NoneBool = None
    reply_to_message_id: NoneInt = None
    allow_sending_without_reply: NoneBool = None
    reply_markup: ReplyMarkup | None = None

    __meth_file_fields__: ClassVar[tuple[str, ...]] = ("voice",)
