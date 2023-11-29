from __future__ import annotations

__all__ = [
    "MenuButton",
    "MenuButtonCommands",
    "MenuButtonDefault",
    "MenuButtonWebApp",
]

from typing import ClassVar
from typing import Literal
from typing import TypeAlias
from typing import final

from .abc import TelegramType
from .web_app_info import WebAppInfo


@final
class MenuButtonCommands(TelegramType, tag="commands"):
    """Represents a menu button, which opens the bot's list of commands.

    See: https://core.telegram.org/bots/api#menubuttoncommands
    """

    type: ClassVar[Literal["commands"]] = "commands"
    """Type of the button, must be `commands`"""


@final
class MenuButtonDefault(TelegramType, tag="default"):
    """Describes that no specific value for the menu button was set.

    See: https://core.telegram.org/bots/api#menubuttondefault
    """

    type: ClassVar[Literal["default"]] = "default"
    """Type of the button, must be `default`."""


@final
class MenuButtonWebApp(TelegramType, tag="web_app"):
    """Represents a menu button, which launches a Web App.

    See: https://core.telegram.org/bots/api#menubuttonwebapp
    """

    text: str
    """Text on the button."""

    web_app: WebAppInfo
    """Description of the Web App that will be launched when the user presses
    the button. The Web App will be able to send an arbitrary message on behalf
    of the user using the method :meth:`yatbaf.bot.Bot.answer_web_app_query`.
    """

    type: ClassVar[Literal["web_app"]] = "web_app"
    """Type of the button, must be `web_app`."""


# https://core.telegram.org/bots/api#menubutton
MenuButton: TypeAlias = (
    "MenuButtonCommands | MenuButtonDefault | MenuButtonWebApp"
)
