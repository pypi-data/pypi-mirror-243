from __future__ import annotations

from typing import final

from yatbaf.typing import NoneStr

from .abc import TelegramType
from .animation import Animation
from .message_entity import MessageEntity
from .photo_size import PhotoSize


@final
class Game(TelegramType):
    """This object represents a game.

    See: https://core.telegram.org/bots/api#game
    """

    title: str
    """Title of the game."""

    description: str
    """Description of the game."""

    photo: list[PhotoSize]
    """Photo that will be displayed in the game message in chats."""

    text: NoneStr = None
    """*Optional.* Brief description of the game or high scores included in the
    game message. Can be automatically edited to include current high scores for
    the game when the bot calls
    :meth:`set_game_score <yatbaf.bot.Bot.set_game_score>`, or manually edited
    using :meth:`edit_message_text <yatbaf.bot.Bot.edit_message_text>`.
    0-4096 characters.
    """

    text_entities: list[MessageEntity] | None = None
    """*Optional.* Special entities that appear in text, such as usernames,
    URLs, bot commands, etc.
    """

    animation: Animation | None = None
    """*Optional.*
    Animation that will be displayed in the game message in chats.
    """
