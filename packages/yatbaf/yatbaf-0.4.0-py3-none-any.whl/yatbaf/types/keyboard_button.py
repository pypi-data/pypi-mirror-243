from __future__ import annotations

__all__ = (
    "KeyboardButton",
    "KeyboardButtonPollType",
    "KeyboardButtonRequestChat",
    "KeyboardButtonRequestUser",
)

from typing import TYPE_CHECKING
from typing import final

from .abc import TelegramType

if TYPE_CHECKING:
    from yatbaf.enums import PollType
    from yatbaf.typing import NoneBool

    from .chat_administrator_rights import ChatAdministratorRights
    from .web_app_info import WebAppInfo


@final
class KeyboardButtonPollType(TelegramType):
    """This object represents type of a poll, which is allowed to be created and
    sent when the corresponding button is pressed.

    See: https://core.telegram.org/bots/api#keyboardbuttonpolltype
    """

    type: PollType | None = None
    """*Optional.* If ``quiz`` is passed, the user will be allowed to create
    only polls in the quiz mode. If ``regular`` is passed, only regular polls
    will be allowed. Otherwise, the user will be allowed to create a poll of
    any type.
    """


@final
class KeyboardButtonRequestChat(TelegramType):
    """This object defines the criteria used to request a suitable chat. The
    identifier of the selected chat will be shared with the bot when the
    corresponding button is pressed.

    See: https://core.telegram.org/bots/api#keyboardbuttonrequestchat
    """

    request_id: int
    """Signed 32-bit identifier of the request, which will be received back in
    the :class:`ChatShared <yatbaf.types.chat_shared.ChatShared>` object.

    .. note::

        Must be unique within the message.
    """

    chat_is_channel: bool
    """Pass ``True`` to request a channel chat, pass ``False`` to request a
    group or a supergroup chat.
    """

    chat_is_forum: NoneBool = None
    """*Optional.* Pass ``True`` to request a forum supergroup, pass ``False``
    to request a non-forum chat. If not specified, no additional restrictions
    are applied.
    """

    chat_has_username: NoneBool = None
    """*Optional.* Pass ``True`` to request a supergroup or a channel with a
    username, pass ``False`` to request a chat without a username. If not
    specified, no additional restrictions are applied.
    """

    chat_is_created: NoneBool = None
    """*Optional.* Pass ``True``. to request a chat owned by the user.
    Otherwise, no additional restrictions are applied.
    """

    user_administrator_rights: ChatAdministratorRights | None = None
    """*Optional.* An object listing the required administrator rights of the
    user in the chat. The rights must be a superset of ``bot_administrator_rights``.
    If not specified, no additional restrictions are applied.
    """  # noqa: E501

    bot_administrator_rights: ChatAdministratorRights | None = None
    """*Optional.* An object listing the required administrator rights of the
    bot in the chat. The rights must be a subset of ``user_administrator_rights``.
    If not specified, no additional restrictions are applied.
    """  # noqa: E501

    bot_is_member: NoneBool = None
    """*Optional.* Pass ``True`` to request a chat with the bot as a member.
    Otherwise, no additional restrictions are applied.
    """


@final
class KeyboardButtonRequestUser(TelegramType):
    """This object defines the criteria used to request a suitable user. The
    identifier of the selected user will be shared with the bot when the
    corresponding button is pressed.

    See: https://core.telegram.org/bots/api#keyboardbuttonrequestuser
    """

    request_id: int
    """Signed 32-bit identifier of the request, which will be received back in
    the :class:`yatbaf.types.user_shared.UserShared` object. Must be unique
    within the message.
    """

    user_is_bot: NoneBool = None
    """*Optional.* Pass ``True`` to request a bot, pass ``False`` to request a
    regular user. If not specified, no additional restrictions are applied.
    """

    user_is_premium: NoneBool = None
    """*Optional.* Pass ``True`` to request a premium user, pass ``False`` to
    request a non-premium user. If not specified, no additional restrictions
    are applied.
    """


@final
class KeyboardButton(TelegramType):
    """This object represents one button of the reply keyboard. For simple text
    buttons, String can be used instead of this object to specify the button
    text.

    .. note::

        The optional fields ``web_app``, ``request_user``, ``request_chat``,
        ``request_contact``, ``request_location``, and ``request_poll`` are
        mutually exclusive.

    See: https://core.telegram.org/bots/api#keyboardbutton
    """

    text: str
    """Text of the button. If none of the optional fields are used, it will be
    sent as a message when the button is pressed.
    """

    request_user: KeyboardButtonRequestUser | None = None
    """*Optional.* If specified, pressing the button will open a list of
    suitable users. Tapping on any user will send their identifier to the bot
    in a “user_shared” service message. Available in private chats only.
    """

    request_chat: KeyboardButtonRequestChat | None = None
    """*Optional.* If specified, pressing the button will open a list of
    suitable chats. Tapping on a chat will send its identifier to the bot in a
    “chat_shared” service message. Available in private chats only.
    """

    request_contact: NoneBool = None
    """*Optional.* If ``True``, the user's phone number will be sent as a
    contact when the button is pressed. Available in private chats only.
    """

    request_location: NoneBool = None
    """*Optional.* If ``True``, the user's current location will be sent when
    the button is pressed. Available in private chats only.
    """

    request_poll: KeyboardButtonPollType | None = None
    """*Optional.* If specified, the user will be asked to create a poll and
    send it to the bot when the button is pressed. Available in private chats
    only.
    """

    web_app: WebAppInfo | None = None
    """*Optional.* If specified, the described Web App will be launched when
    the button is pressed. The Web App will be able to send a “web_app_data”
    service message. Available in private chats only.
    """
