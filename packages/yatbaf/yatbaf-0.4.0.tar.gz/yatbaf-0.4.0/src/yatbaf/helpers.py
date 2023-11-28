from __future__ import annotations

__all__ = (
    "parse_command_args",
    "md",
    "create_user_link",
    "create_bot_deeplink",
    "create_group_deeplink",
    "create_channel_deeplink",
    "create_game_deeplink",
    "create_webapp_deeplink",
)

import re
from typing import TYPE_CHECKING
from typing import final

from .enums import MarkdownEntity
from .utils import is_valid_deeplink_parameter
from .utils import is_valid_username

if TYPE_CHECKING:
    from typing import Final

    from .enums import AdminFlag
    from .typing import NoneStr


def parse_command_args(text: str) -> list[str]:
    """Parse command args.

    :param text: Message with command.
    """

    return sp[-1].split() if len(sp := text.split(maxsplit=1)) == 2 else []


@final
class md:
    """Markdown formatting.

    See: https://core.telegram.org/bots/api#markdownv2-style

    .. important::

        MarkdownV2 style only.
    """

    # yapf: disable
    REPL: Final[str] = r"\\\1"
    """:meta private:"""
    PATTERN_TEXT: Final[re.Pattern] = re.compile(f'([{re.escape(r"_*[]()~`>#+-=|{}.!")}])')  # noqa: E501
    """:meta private:"""
    PATTERN_FSTRING: Final[re.Pattern] = re.compile(f'([{re.escape(r"_*[]()~`>#+-=|.!")}])')  # noqa: E501
    """:meta private:"""
    PATTERN_CODE_PRE: Final[re.Pattern] = re.compile(r"([\\\`])")
    """:meta private:"""
    PATTERN_LINK_EMOJI: Final[re.Pattern] = re.compile(r"([\\\\\)])")
    """:meta private:"""
    # yapf: enable

    # yapf: disable
    @staticmethod
    def escape(
        text: str, /, entity: MarkdownEntity | str = MarkdownEntity.TEXT
    ) -> str:
        """Use this method to escape markdown characters in text."""

        # yapf: enable
        entity = str(entity)
        if entity == "fstring":
            return md.PATTERN_FSTRING.sub(md.REPL, text)

        if entity in ["link", "emoji"]:
            return md.PATTERN_LINK_EMOJI.sub(md.REPL, text)

        if entity in ["code", "pre"]:
            return md.PATTERN_CODE_PRE.sub(md.REPL, text)

        return md.PATTERN_TEXT.sub(md.REPL, text)

    @staticmethod
    def bold(text: str, /) -> str:
        return f"*{text}*"

    @staticmethod
    def italic(text: str, /) -> str:
        return f"_{text}_"

    @staticmethod
    def underline(text: str, /) -> str:
        return f"__{text}__"

    @staticmethod
    def strikethrough(text: str, /) -> str:
        return f"~{text}~"

    @staticmethod
    def spoiler(text: str, /) -> str:
        return f"||{text}||"

    @staticmethod
    def url(text: str, url: str, /) -> str:
        return f"[{text}]({url})"

    @staticmethod
    def mention(username: str, user_id: int, /) -> str:
        return f"[{username}](tg://user?id={user_id})"

    @staticmethod
    def emoji(emoji_id: int, placeholder_emoji: str, /) -> str:
        return f"![{placeholder_emoji}](tg://emoji?id={emoji_id})"

    @staticmethod
    def inline(text: str, /) -> str:
        return f"`{text}`"

    @staticmethod
    def code(text: str, /, lang: str = "") -> str:
        return f"```{lang}\n{text}\n```"


def create_user_link(username: str) -> str:
    """Returns link used to share public users, groups and channels

    See: https://core.telegram.org/api/links#public-username-links

    :param username: Public username.
    :raises ValueError: if username contains invalid chars.
    """

    if not is_valid_username(username):
        raise ValueError("Username is invalid.")
    return f"https://t.me/{username}"


def _check_deeplink_parameter(parameter: str) -> None:
    if not is_valid_deeplink_parameter(parameter):
        raise ValueError(
            "`parameter` can contain only following characters: "
            "a-z, A-Z, 0-9, '_', '-'"
        )


def create_bot_deeplink(bot_username: str, parameter: NoneStr = None) -> str:
    """Returns deep link used to link to bots.

    See: https://core.telegram.org/api/links#bot-links

    :param bot_username: Bot username.
    :param parameter: Start parameter, up to 64 base64url characters: if
        provided and the bot_username is indeed a bot, the text input bar should
        be replaced with a Start button (even if the user has already started
        the bot) that should invoke messages.startBot with the appropriate
        parameter once clicked.
    :raises ValueError: if ``bot_username`` or ``parameter`` contains invalid
        chars.
    """

    link = create_user_link(bot_username)
    if parameter:
        _check_deeplink_parameter(parameter)
        link += f"?start={parameter}"

    return link


def create_group_deeplink(
    bot_username: str,
    parameter: NoneStr = None,
    admin: list[AdminFlag] | None = None,
) -> str:
    """Returns deep link used to add bots to groups.

    See: https://core.telegram.org/api/links#groupchannel-bot-links

    :param bot_username: Bot username
    :param parameter: *Optional.* Start parameter, up to 64 base64url
        characters: if provided and the bot_username is indeed a bot,
        messages.startBot with the appropriate parameter should be invoked after
        adding the bot to the group.
    :param admin: *Optional.* A list of identifiers.
    :raises ValueError: if ``bot_username`` or ``parameter`` contains invalid
        chars.
    """

    link = create_user_link(bot_username) + "?startgroup"
    if parameter:
        _check_deeplink_parameter(parameter)
        link += f"={parameter}"

    if admin:
        link += f"&admin={'+'.join(admin)}"

    return link


def create_channel_deeplink(
    bot_username: str,
    admin: list[AdminFlag],
) -> str:
    """Returns deep link used to add bots to channels.

    See: https://core.telegram.org/api/links#groupchannel-bot-links

    :param bot_username: Bot username
    :param admin: A list of identifiers.
    :raises ValueError: if ``bot_username`` contains invalid chars or ``admin``
        is empty.
    """

    if not admin:
        raise ValueError("`admin` can't be empty.")

    return (
        create_user_link(bot_username) +
        f"?startchannel&admin={'+'.join(admin)}"
    )


def create_game_deeplink(bot_username: str, short_name: str) -> str:
    """Returns deep link used to share games.

    See: https://core.telegram.org/api/links#game-links

    :param bot_username: Username of the bot that owns the game.
    :param short_name: Game short name.
    :raises ValueError: if ``bot_username`` contains invalid chars.
    """

    return create_user_link(bot_username) + f"?game={short_name}"


def create_webapp_deeplink(
    bot_username: str,
    short_name: str,
    parameter: NoneStr = None,
) -> str:
    """Returns deep link used to share named bot web apps.

    See: https://core.telegram.org/api/links#named-bot-web-app-links

    :param bot_username: Username of the bot that owns the web app.
    :param short_name: Web app short name.
    :param parameter: *Optional.* `start_param` to pass to
        messages.requestAppWebView.
    :raises ValueError: if ``bot_username`` or ``parameter`` contains invalid
        chars.
    """

    link = create_user_link(bot_username) + f"/{short_name}?startapp"
    if parameter:
        _check_deeplink_parameter(parameter)
        link += f"={parameter}"

    return link
