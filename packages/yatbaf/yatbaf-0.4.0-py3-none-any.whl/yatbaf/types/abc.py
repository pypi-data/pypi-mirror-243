from __future__ import annotations

__all__ = ("TelegramType",)

from typing import TYPE_CHECKING
from typing import Any
from typing import ClassVar
from typing import cast

from msgspec import Struct

if TYPE_CHECKING:
    from yatbaf.bot import Bot


class _usrctx:  # noqa: N801
    """:meta private:"""

    __slots__ = ("__usrctx__",)


class TelegramType(_usrctx, Struct, omit_defaults=True):
    """Base class for Telegram types"""

    __usrctx__: ClassVar[dict[str, Any]]

    def __post_init__(self) -> None:  # pragma: no cover
        self.__usrctx__ = {}  # type: ignore[misc]

    def __str__(self) -> str:  # pragma: no cover
        return self.__class__.__name__.lower()

    @property
    def ctx(self) -> dict[str, Any]:
        """Dict object.

        Use it to share data between middleware/handler in request context::

            @router.guard
            async def guard(update):
                update.ctx["foo"] = "bar"
                return True

            @router.middleware
            def middleware(handler):
                async def wrapper(update):
                    update.ctx["foo"] += "baz"
                    await handler(update)
                return wrapper

            @router
            async def handler(update):
                assert update.ctx["foo"] == "barbaz"
        """

        return self.__usrctx__

    @property
    def bot(self) -> Bot:
        """Bot instance.

        Use it to get access to :class:`Bot <yatbaf.bot.Bot>` instance inside
        handler function::

            @on_message
            async def handler(message: Message) -> None:
                await message.bot.leave_chat(message.chat.id)
        """

        try:
            return cast("Bot", self.__usrctx__["__bot_obj__"])
        except KeyError:
            raise RuntimeError("Bot not bound to this instance.") from None

    def _bind_bot_obj(self, bot: Bot) -> None:
        self.__usrctx__["__bot_obj__"] = bot

        for field_name in self.__struct_fields__:
            field = getattr(self, field_name)
            if isinstance(field, TelegramType):
                field._bind_bot_obj(bot)
