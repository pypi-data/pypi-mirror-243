from __future__ import annotations

from typing import final

from yatbaf.typing import NoneBool
from yatbaf.typing import NoneStr

from .abc import TelegramType
from .keyboard_button import KeyboardButton


@final
class ReplyKeyboardMarkup(TelegramType):
    """This object represents a custom keyboard with reply options.

    See: https://core.telegram.org/bots/api#replykeyboardmarkup
    """

    keyboard: list[list[KeyboardButton]]
    """List of button rows, each represented by an list of
    :class:`KyeboardButton <yatbaf.types.keyboard_button.KeyboardButton>`
    objects.
    """

    is_persistent: NoneBool = None
    """*Optional.* Requests clients to always show the keyboard when the regular
    keyboard is hidden. Defaults to ``False``, in which case the custom keyboard
    can be hidden and opened with a keyboard icon.
    """

    resize_keyboard: NoneBool = None
    """*Optional.* Requests clients to resize the keyboard vertically for
    optimal fit (e.g., make the keyboard smaller if there are just two rows of
    buttons). Defaults to ``False``, in which case the custom keyboard is always
    of the same height as the app's standard keyboard.
    """

    one_time_keyboard: NoneBool = None
    """*Optional.* Requests clients to hide the keyboard as soon as it's been
    used. The keyboard will still be available, but clients will automatically
    display the usual letter-keyboard in the chat - the user can press a special
    button in the input field to see the custom keyboard again. Defaults to
    ``False``.
    """

    input_field_placeholder: NoneStr = None
    """*Optional.* The placeholder to be shown in the input field when the
    keyboard is active; 1-64 characters.
    """

    selective: NoneBool = None
    """*Optional.* Use this parameter if you want to show the keyboard to
    specific users only. Targets: 1) users that are @mentioned in the text of
    the Message object; 2) if the bot's message is a reply (has
    ``reply_to_message_id``), sender of the original message.
    """
