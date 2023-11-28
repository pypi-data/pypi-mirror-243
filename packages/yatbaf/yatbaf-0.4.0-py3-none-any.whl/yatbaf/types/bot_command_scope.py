from __future__ import annotations

__all__ = (
    "BotCommandScopeAllChatAdministrators",
    "BotCommandScopeAllGroupChats",
    "BotCommandScopeAllPrivateChats",
    "BotCommandScopeChat",
    "BotCommandScopeChatAdministrators",
    "BotCommandScopeChatMember",
    "BotCommandScopeDefault",
    "BotCommandScope",
)

from typing import Literal
from typing import TypeAlias
from typing import final

from msgspec import field

from .abc import TelegramType


@final
class BotCommandScopeAllChatAdministrators(TelegramType):
    """Represents the scope of bot commands, covering all group and supergroup
    chat administrators.

    See: https://core.telegram.org/bots/api#botcommandscopeallchatadministrators
    """

    type: Literal["all_chat_administrators"] = field(
        default_factory=lambda: "all_chat_administrators"
    )
    """Scope type, must be `all_chat_administrators`."""


@final
class BotCommandScopeAllGroupChats(TelegramType):
    """Represents the scope of bot commands, covering all group and supergroup
    chats.

    See: https://core.telegram.org/bots/api#botcommandscopeallgroupchats
    """

    type: Literal["all_group_chats"] = field(
        default_factory=lambda: "all_group_chats"
    )
    """Scope type, must be `all_group_chats`."""


@final
class BotCommandScopeAllPrivateChats(TelegramType):
    """Represents the scope of bot commands, covering all private chats.

    See: https://core.telegram.org/bots/api#botcommandscopeallprivatechats
    """

    type: Literal["all_private_chats"] = field(
        default_factory=lambda: "all_private_chats"
    )
    """Scope type, must be `all_private_chats`."""


@final
class BotCommandScopeChat(TelegramType):
    """Represents the scope of bot commands, covering a specific chat.

    See: https://core.telegram.org/bots/api#botcommandscopechat
    """

    chat_id: int | str
    """Unique identifier for the target chat or username of the target
    supergroup (in the format @supergroupusername).
    """

    type: Literal["chat"] = field(default_factory=lambda: "chat")
    """Scope type, must be `chat`."""


@final
class BotCommandScopeChatAdministrators(TelegramType):
    """Represents the scope of bot commands, covering all administrators of a
    specific group or supergroup chat.

    See: https://core.telegram.org/bots/api#botcommandscopechatadministrators
    """

    chat_id: int | str
    """Unique identifier for the target chat or username of the target
    supergroup (in the format @supergroupusername).
    """

    type: Literal["chat_administrators"] = field(
        default_factory=lambda: "chat_administrators"
    )
    """Scope type, must be `chat_administrators`."""


@final
class BotCommandScopeChatMember(TelegramType):
    """Represents the scope of bot commands, covering a specific member of a
    group or supergroup chat.

    See: https://core.telegram.org/bots/api#botcommandscopechatmember
    """

    chat_id: int | str
    """Unique identifier for the target chat or username of the target
    supergroup (in the format @supergroupusername).
    """

    user_id: int
    """Unique identifier of the target user."""

    type: Literal["chat_member"] = field(default_factory=lambda: "chat_member")
    """Scope type, must be `chat_member`."""


@final
class BotCommandScopeDefault(TelegramType):
    """Represents the default scope of bot commands. Default commands are used
    if no commands with a narrower scope are specified for the user.

    See: https://core.telegram.org/bots/api#botcommandscopedefault
    """

    type: Literal["default"] = field(default_factory=lambda: "default")
    """Scope type, must be `default`."""


# https://core.telegram.org/bots/api#botcommandscope
BotCommandScope: TypeAlias = (
    "BotCommandScopeAllChatAdministrators "
    "| BotCommandScopeAllGroupChats "
    "| BotCommandScopeAllPrivateChats "
    "| BotCommandScopeChat "
    "| BotCommandScopeChatAdministrators "
    "| BotCommandScopeChatMember "
    "| BotCommandScopeDefault"
)
