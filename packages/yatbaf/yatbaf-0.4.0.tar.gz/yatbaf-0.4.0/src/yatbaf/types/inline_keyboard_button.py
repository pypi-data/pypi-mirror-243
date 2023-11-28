from __future__ import annotations

from typing import final

from yatbaf.typing import NoneBool
from yatbaf.typing import NoneStr

from .abc import TelegramType
from .callback_game import CallbackGame
from .login_url import LoginUrl
from .switch_inline_query_chosen_chat import SwitchInlineQueryChosenChat
from .web_app_info import WebAppInfo


@final
class InlineKeyboardButton(TelegramType):
    """This object represents one button of an inline keyboard.

    .. note::

        You **must** use exactly one of the optional fields.

    See: https://core.telegram.org/bots/api#inlinekeyboardbutton
    """

    text: str
    """Label text on the button."""

    url: NoneStr = None
    """*Optional.* HTTP or tg:// URL to be opened when the button is pressed.
    Links tg://user?id=<user_id> can be used to mention a user by their ID
    without using a username, if this is allowed by their privacy settings.
    """

    callback_data: NoneStr = None
    """*Optional.* Data to be sent in a callback query to the bot when button
    is pressed, 1-64 bytes.
    """

    web_app: WebAppInfo | None = None
    """*Optional.* Description of the Web App that will be launched when the
    user presses the button. The Web App will be able to send an arbitrary
    message on behalf of the user using the method
    :meth:`yatbaf.bot.Bot.answer_web_app_query()`.

    .. note::

        Available only in private chats between a user and the bot.
    """

    login_url: LoginUrl | None = None
    """*Optional.* An HTTPS URL used to automatically authorize the user."""

    switch_inline_query: NoneStr = None
    """*Optional.* If set, pressing the button will prompt the user to select
    one of their chats, open that chat and insert the bot's username and the
    specified inline query in the input field. May be empty, in which case just
    the bot's username will be inserted.
    """

    switch_inline_query_current_chat: NoneStr = None
    """*Optional.* If set, pressing the button will insert the bot's username
    and the specified inline query in the current chat's input field. May be
    empty, in which case only the bot's username will be inserted.
    """

    switch_inline_query_chosen_chat: SwitchInlineQueryChosenChat | None = None
    """*Optional.* If set, pressing the button will prompt the user to select
    one of their chats of the specified type, open that chat and insert the
    bot's username and the specified inline query in the input field.
    """

    callback_game: CallbackGame | None = None
    """*Optional.* Description of the game that will be launched when the user
    presses the button.

    .. important::

        This type of button *must* always be the first button in the first row.
    """

    pay: NoneBool = None
    """*Optional.* Specify True, to send a Pay button.

    .. important::

        This type of button must always be the first button in the first row
        and can only be used in invoice messages.
    """
