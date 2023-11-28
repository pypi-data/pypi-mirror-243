from __future__ import annotations

from typing import TYPE_CHECKING
from typing import final

from yatbaf.types import Message

from .abc import TelegramMethodWithMedia

if TYPE_CHECKING:
    from yatbaf.types import InputMediaAudio
    from yatbaf.types import InputMediaDocument
    from yatbaf.types import InputMediaPhoto
    from yatbaf.types import InputMediaVideo
    from yatbaf.typing import NoneBool
    from yatbaf.typing import NoneInt


@final
class SendMediaGroup(TelegramMethodWithMedia[list[Message]]):
    """See :meth:`yatbaf.bot.Bot.send_media_group`"""

    chat_id: str | int
    # yapf: disable
    media: list[InputMediaAudio | InputMediaDocument | InputMediaPhoto | InputMediaVideo]  # noqa: E501
    # yapf: enable
    message_thread_id: NoneInt = None
    disable_notification: NoneBool = None
    protect_content: NoneBool = None
    reply_to_message_id: NoneInt = None
    allow_sending_without_reply: NoneBool = None
