from __future__ import annotations

from typing import final

from msgspec import field

from yatbaf.typing import NoneBool
from yatbaf.typing import NoneInt
from yatbaf.typing import NoneStr

from .abc import TelegramType
from .message import Message
from .user import User


@final
class CallbackQuery(TelegramType, kw_only=True):
    """This object represents an incoming callback query from a callback button
    in an inline keyboard. If the button that originated the query was attached
    to a message sent by the bot, the field ``message`` will be present. If the
    button was attached to a message sent via the bot (in inline mode), the
    field ``inline_message_id`` will be present. Exactly one of the fields data
    or ``game_short_name`` will be present.

    See: https://core.telegram.org/bots/api#callbackquery
    """

    id: str
    """Unique identifier for this query"""

    from_: User = field(name="from")
    """Sender"""

    message: Message | None = None
    """*Optional.* Message with the callback button that originated the query.
    Note that message content and message date will not be available if the
    message is too old.
    """

    inline_message_id: NoneStr = None
    """*Optional.* Identifier of the message sent via the bot in inline mode,
    that originated the query.
    """

    chat_instance: str
    """Global identifier, uniquely corresponding to the chat to which the
    message with the callback button was sent. Useful for high scores in games.
    """

    data: NoneStr = None
    """*Optional.* Data associated with the callback button. Be aware that the
    message originated the query can contain no callback buttons with this data.
    """

    game_short_name: NoneStr = None
    """*Optional.* Short name of a `Game`_ to be returned, serves as the unique
    identifier for the game.

    .. _game: https://core.telegram.org/bots/api#games
    """

    async def answer(
        self,
        text: NoneStr = None,
        show_alert: NoneBool = None,
        url: NoneStr = None,
        cache_time: NoneInt = None,
    ) -> bool:
        """Use this method to send answer to callback.

        See: :meth:`Bot.answer_callback_query <yatbaf.bot.Bot.answer_callback_query>`
        """  # noqa: E501

        return await self.bot.answer_callback_query(
            callback_query_id=self.id,
            text=text,
            show_alert=show_alert,
            url=url,
            cache_time=cache_time,
        )
