from __future__ import annotations

__all__ = ("chat_action",)

import asyncio
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .enums import ChatAction
    from .types import Message
    from .typing import HandlerFunc
    from .typing import Middleware


def chat_action(action: ChatAction) -> Middleware[Message]:
    """Send chat action and automatically update it if your operation takes
    more than 5 seconds to complete.

    Usage::

        @on_message(middleware=[chat_action(ChatAction.UPLOAD_PHOTO)])
        async def slow_operation(message: Message) -> None:
            ...

    See: :class:`ChatAction <yatbaf.enums.ChatAction>`

    :param action: Chat action.
    """

    def outer(handler: HandlerFunc[Message]) -> HandlerFunc[Message]:

        async def inner(update: Message) -> None:
            event = asyncio.Event()

            async def _task() -> None:
                while not event.is_set():
                    await update.bot.send_chat_action(update.chat.id, action)
                    await asyncio.sleep(4.5)  # update status every 4.5 sec

            update.bot.tasks.add(
                _task(),
                name=f"chat-action-{update.message_id}",
            )
            try:
                await handler(update)
            finally:
                event.set()

        return inner

    return outer
