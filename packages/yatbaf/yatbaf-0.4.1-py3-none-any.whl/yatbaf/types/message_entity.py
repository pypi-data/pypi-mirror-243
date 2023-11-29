from __future__ import annotations

from typing import final

from yatbaf.enums import MessageEntityType
from yatbaf.typing import NoneStr

from .abc import TelegramType
from .user import User


@final
class MessageEntity(TelegramType):
    """This object represents one special entity in a text message. For example,
    hashtags, usernames, URLs, etc.

    See: https://core.telegram.org/bots/api#messageentity
    """

    type: MessageEntityType
    """Type of the entity."""

    offset: int
    """Offset in UTF-16 code units to the start of the entity."""

    length: int
    """Length of the entity in UTF-16 code units."""

    url: NoneStr = None
    """*Optional.* For :attr:`yatbaf.enums.MessageEntityType.TEXT_LINK` only,
    URL that will be opened after user taps on the text.
    """

    user: User | None = None
    """*Optional.* For :attr:`yatbaf.enums.MessageEntityType.TEXT_MENTION`
    only, the mentioned user.
    """

    language: NoneStr = None
    """*Optional.* For :attr:`yatbaf.enums.MessageEntityType.PRE` only, the
    programming language of the entity text.
    """

    custom_emoji_id: NoneStr = None
    """*Optional.* For :attr:`yatbaf.enums.MessageEntityType.CUSTOM_EMOJI`
    only, unique identifier of the custom emoji. Use
    :meth:`get_custom_emoji_stickers <yatbaf.bot.Bot.get_custom_emoji_stickers>`
    to get full information about the sticker.
    """  # noqa: E501
