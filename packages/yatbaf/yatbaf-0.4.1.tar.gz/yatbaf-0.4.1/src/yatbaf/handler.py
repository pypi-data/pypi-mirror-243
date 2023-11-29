from __future__ import annotations

__all__ = (
    "Handler",
    "on_message",
    "on_edited_message",
    "on_channel_post",
    "on_edited_channel_post",
    "on_inline_query",
    "on_chosen_inline_result",
    "on_callback_query",
    "on_shipping_query",
    "on_pre_checkout_query",
    "on_poll",
    "on_poll_answer",
    "on_my_chat_member",
    "on_chat_member",
    "on_chat_join_request",
)

from typing import TYPE_CHECKING
from typing import Generic
from typing import TypeAlias
from typing import TypeVar
from typing import final
from typing import overload

from .enums import UpdateType
from .typing import UpdateT
from .utils import ensure_unique

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Sequence

    from .abc import AbstractRouter
    from .types import CallbackQuery
    from .types import ChatJoinRequest
    from .types import ChatMemberUpdated
    from .types import ChosenInlineResult
    from .types import InlineQuery
    from .types import Message
    from .types import Poll
    from .types import PollAnswer
    from .types import PreCheckoutQuery
    from .types import ShippingQuery
    from .typing import Filter
    from .typing import HandlerFunc
    from .typing import Middleware


@final
class Handler(Generic[UpdateT]):
    """Handler object.

    :param fn: Handler function.
    :param update_type: Handler update type. See :class:`yatbaf.enums.UpdateType`
    :param middleware: *Optional.* A sequence of
        :class:`Middleware <yatbaf.typing.Middleware>`.
    :param filters: *Optional.* A sequence of
        :class:`Filter <yatbaf.typing.Filter>`.
    :param sort_filters: Pass ``False`` if you want to use your filter order.
        Default ``True``.
    :param any_filter: Pass ``True`` if matching one of the filters is enough.
        Default ``False``.
    """  # noqa: E501

    __slots__ = (
        "_fn",
        "_filters",
        "_middleware",
        "_update_type",
        "_parent",
        "_match_fn",
        "_middleware_stack",
    )

    _middleware_stack: HandlerFunc[UpdateT]

    def __init__(
        self,
        fn: HandlerFunc[UpdateT],
        update_type: UpdateType | str,
        *,
        middleware: Sequence[Middleware[UpdateT]] | None = None,
        filters: Sequence[Filter[UpdateT]] | None = None,
        sort_filters: bool = True,
        any_filter: bool = False,
    ) -> None:
        self._fn = fn
        self._update_type = update_type
        self._match_fn = all if not any_filter else any
        self._parent: AbstractRouter | None = None

        self._filters: list[Filter[UpdateT]] = []
        # yapf: disable
        self._middleware: list[Middleware[UpdateT]] = ensure_unique(
            middleware or []
        )
        # yapf: enable
        self._register_filters(filters or [], sort_filters)

    def __repr__(self) -> str:
        return f"<Handler[type={self._update_type}]>"

    async def __call__(self, update: UpdateT, /) -> None:
        """Execute middleware and handler.

        :param update: Incoming update.
        """
        await self._middleware_stack(update)

    @property
    def orig(self) -> HandlerFunc[UpdateT]:
        """Original function."""
        return self._fn

    @property
    def update_type(self) -> UpdateType | str:
        """Handler type."""
        return self._update_type

    def _register_filters(
        self, filters: Sequence[Filter[UpdateT]], sort_filters: bool
    ) -> None:
        for func in filters:
            if func not in self._filters:
                self._filters.append(func)
        if sort_filters:
            self._filters.sort(key=lambda v: v.priority)

    def _build_middleware_stack(self) -> HandlerFunc[UpdateT]:
        middleware_stack = self._fn
        router: AbstractRouter | Handler | None = self
        while router is not None:
            for func in reversed(router._middleware):
                middleware_stack = func(middleware_stack)
            router = router._parent
        return middleware_stack

    def _on_registration(self) -> None:
        self._middleware_stack = self._build_middleware_stack()

    def _match(self, update: UpdateT, /) -> bool:
        return self._match_fn(f.check(update) for f in self._filters)

    def _is_fallback(self) -> bool:
        return not bool(self._filters)


T = TypeVar("T")
Wrapper: TypeAlias = "Callable[[HandlerFunc[T]], Handler[T]]"


@overload
def on_message(__fn: HandlerFunc[Message]) -> Handler[Message]:
    ...


@overload
def on_message(
    *,
    filters: Sequence[Filter[Message]] | None = None,
    middleware: Sequence[Middleware[Message]] | None = None,
    sort_filters: bool = True,
    any_filter: bool = False,
) -> Wrapper[Message]:
    ...


def on_message(
    __fn: HandlerFunc[Message] | None = None,
    *,
    filters: Sequence[Filter[Message]] | None = None,
    middleware: Sequence[Middleware[Message]] | None = None,
    sort_filters: bool = True,
    any_filter: bool = False,
) -> Wrapper[Message] | Handler[Message]:
    """Message handler decorator.

    Use this decorator to decorate handler for `message` update.

    See :class:`Handler` for parameters.
    """

    def wrapper(fn: HandlerFunc[Message]) -> Handler[Message]:
        handler: Handler[Message] = Handler(
            fn=fn,
            update_type=UpdateType.MESSAGE,
            filters=filters,
            middleware=middleware,
            sort_filters=sort_filters,
            any_filter=any_filter,
        )
        return handler

    if __fn is None:
        return wrapper
    return wrapper(__fn)


@overload
def on_edited_message(__fn: HandlerFunc[Message]) -> Handler[Message]:
    ...


@overload
def on_edited_message(
    *,
    filters: Sequence[Filter[Message]] | None = None,
    middleware: Sequence[Middleware[Message]] | None = None,
    sort_filters: bool = True,
    any_filter: bool = False,
) -> Wrapper[Message]:
    ...


def on_edited_message(
    __fn: HandlerFunc[Message] | None = None,
    *,
    filters: Sequence[Filter[Message]] | None = None,
    middleware: Sequence[Middleware[Message]] | None = None,
    sort_filters: bool = True,
    any_filter: bool = False,
) -> Wrapper[Message] | Handler[Message]:
    """Edited message handler decorator.

    Use this decorator to decorate handler for `edited_message` update.

    See :class:`Handler` for parameters.
    """

    def wrapper(fn: HandlerFunc[Message]) -> Handler[Message]:
        handler: Handler[Message] = Handler(
            fn=fn,
            update_type=UpdateType.EDITED_MESSAGE,
            filters=filters,
            middleware=middleware,
            sort_filters=sort_filters,
            any_filter=any_filter,
        )
        return handler

    if __fn is None:
        return wrapper
    return wrapper(__fn)


@overload
def on_channel_post(__fn: HandlerFunc[Message]) -> Handler[Message]:
    ...


@overload
def on_channel_post(
    *,
    filters: Sequence[Filter[Message]] | None = None,
    middleware: Sequence[Middleware[Message]] | None = None,
    sort_filters: bool = True,
    any_filter: bool = False,
) -> Wrapper[Message]:
    ...


def on_channel_post(
    __fn: HandlerFunc[Message] | None = None,
    *,
    filters: Sequence[Filter[Message]] | None = None,
    middleware: Sequence[Middleware[Message]] | None = None,
    sort_filters: bool = True,
    any_filter: bool = False,
) -> Wrapper[Message] | Handler[Message]:
    """Channel post handler decorator.

    Use this decorator to decorate handler for `channel_post` update.

    See :class:`Handler` for parameters.
    """

    def wrapper(fn: HandlerFunc[Message]) -> Handler[Message]:
        handler: Handler[Message] = Handler(
            fn=fn,
            update_type=UpdateType.CHANNEL_POST,
            filters=filters,
            middleware=middleware,
            sort_filters=sort_filters,
            any_filter=any_filter,
        )
        return handler

    if __fn is None:
        return wrapper
    return wrapper(__fn)


@overload
def on_edited_channel_post(__fn: HandlerFunc[Message]) -> Handler[Message]:
    ...


@overload
def on_edited_channel_post(
    *,
    filters: Sequence[Filter[Message]] | None = None,
    middleware: Sequence[Middleware[Message]] | None = None,
    sort_filters: bool = True,
    any_filter: bool = False,
) -> Wrapper[Message]:
    ...


def on_edited_channel_post(
    __fn: HandlerFunc[Message] | None = None,
    *,
    filters: Sequence[Filter[Message]] | None = None,
    middleware: Sequence[Middleware[Message]] | None = None,
    sort_filters: bool = True,
    any_filter: bool = False,
) -> Wrapper[Message] | Handler[Message]:
    """Edited channel post handler decorator.

    Use this decorator to decorate handler for `edited_channel_post` update.

    See :class:`Handler` for parameters.
    """

    def wrapper(fn: HandlerFunc[Message]) -> Handler[Message]:
        handler: Handler[Message] = Handler(
            fn=fn,
            update_type=UpdateType.EDITED_CHANNEL_POST,
            filters=filters,
            middleware=middleware,
            sort_filters=sort_filters,
            any_filter=any_filter,
        )
        return handler

    if __fn is None:
        return wrapper
    return wrapper(__fn)


@overload
def on_inline_query(__fn: HandlerFunc[InlineQuery]) -> Handler[InlineQuery]:
    ...


@overload
def on_inline_query(
    *,
    filters: Sequence[Filter[InlineQuery]] | None = None,
    middleware: Sequence[Middleware[InlineQuery]] | None = None,
    sort_filters: bool = True,
    any_filter: bool = False,
) -> Wrapper[InlineQuery]:
    ...


def on_inline_query(
    __fn: HandlerFunc[InlineQuery] | None = None,
    *,
    filters: Sequence[Filter[InlineQuery]] | None = None,
    middleware: Sequence[Middleware[InlineQuery]] | None = None,
    sort_filters: bool = True,
    any_filter: bool = False,
) -> Wrapper[InlineQuery] | Handler[InlineQuery]:
    """Inline query handler decorator.

    Use this decorator to decorate handler for `inline_query` update.

    See :class:`Handler` for parameters.
    """

    def wrapper(fn: HandlerFunc[InlineQuery]) -> Handler[InlineQuery]:
        handler: Handler[InlineQuery] = Handler(
            fn=fn,
            update_type=UpdateType.INLINE_QUERY,
            filters=filters,
            middleware=middleware,
            sort_filters=sort_filters,
            any_filter=any_filter,
        )
        return handler

    if __fn is None:
        return wrapper
    return wrapper(__fn)


@overload
def on_chosen_inline_result(
    __fn: HandlerFunc[ChosenInlineResult]
) -> Handler[ChosenInlineResult]:
    ...


@overload
def on_chosen_inline_result(
    *,
    filters: Sequence[Filter[ChosenInlineResult]] | None = None,
    middleware: Sequence[Middleware[ChosenInlineResult]] | None = None,
    sort_filters: bool = True,
    any_filter: bool = False,
) -> Wrapper[ChosenInlineResult]:
    ...


def on_chosen_inline_result(
    __fn: HandlerFunc[ChosenInlineResult] | None = None,
    *,
    filters: Sequence[Filter[ChosenInlineResult]] | None = None,
    middleware: Sequence[Middleware[ChosenInlineResult]] | None = None,
    sort_filters: bool = True,
    any_filter: bool = False,
) -> Wrapper[ChosenInlineResult] | Handler[ChosenInlineResult]:
    """Chosen inline result handler decorator.

    Use this decorator to decorate handler for `chosen_inline_result` update.

    See :class:`Handler` for parameters.
    """

    def wrapper(
        fn: HandlerFunc[ChosenInlineResult]
    ) -> Handler[ChosenInlineResult]:
        handler: Handler[ChosenInlineResult] = Handler(
            fn=fn,
            update_type=UpdateType.CHOSEN_INLINE_RESULT,
            filters=filters,
            middleware=middleware,
            sort_filters=sort_filters,
            any_filter=any_filter,
        )
        return handler

    if __fn is None:
        return wrapper
    return wrapper(__fn)


@overload
def on_callback_query(
    __fn: HandlerFunc[CallbackQuery]
) -> Handler[CallbackQuery]:
    ...


@overload
def on_callback_query(
    *,
    filters: Sequence[Filter[CallbackQuery]] | None = None,
    middleware: Sequence[Middleware[CallbackQuery]] | None = None,
    sort_filters: bool = True,
    any_filter: bool = False,
) -> Wrapper[CallbackQuery]:
    ...


def on_callback_query(
    __fn: HandlerFunc[CallbackQuery] | None = None,
    *,
    filters: Sequence[Filter[CallbackQuery]] | None = None,
    middleware: Sequence[Middleware[CallbackQuery]] | None = None,
    sort_filters: bool = True,
    any_filter: bool = False,
) -> Wrapper[CallbackQuery] | Handler[CallbackQuery]:
    """Callback query handler decorator.

    Use this decorator to decorate handler for `callback_query` update.

    See :class:`Handler` for parameters.
    """

    def wrapper(fn: HandlerFunc[CallbackQuery]) -> Handler[CallbackQuery]:
        handler: Handler[CallbackQuery] = Handler(
            fn=fn,
            update_type=UpdateType.CALLBACK_QUERY,
            filters=filters,
            middleware=middleware,
            sort_filters=sort_filters,
            any_filter=any_filter,
        )
        return handler

    if __fn is None:
        return wrapper
    return wrapper(__fn)


@overload
def on_shipping_query(
    __fn: HandlerFunc[ShippingQuery]
) -> Handler[ShippingQuery]:
    ...


@overload
def on_shipping_query(
    *,
    filters: Sequence[Filter[ShippingQuery]] | None = None,
    middleware: Sequence[Middleware[ShippingQuery]] | None = None,
    sort_filters: bool = True,
    any_filter: bool = False,
) -> Wrapper[ShippingQuery]:
    ...


def on_shipping_query(
    __fn: HandlerFunc[ShippingQuery] | None = None,
    *,
    filters: Sequence[Filter[ShippingQuery]] | None = None,
    middleware: Sequence[Middleware[ShippingQuery]] | None = None,
    sort_filters: bool = True,
    any_filter: bool = False,
) -> Wrapper[ShippingQuery] | Handler[ShippingQuery]:
    """Shipping query handler decorator.

    Use this decorator to decorate handler for `shipping_query` update.

    See :class:`Handler` for parameters.
    """

    def wrapper(fn: HandlerFunc[ShippingQuery]) -> Handler[ShippingQuery]:
        handler: Handler[ShippingQuery] = Handler(
            fn=fn,
            update_type=UpdateType.SHIPPING_QUERY,
            filters=filters,
            middleware=middleware,
            sort_filters=sort_filters,
            any_filter=any_filter,
        )
        return handler

    if __fn is None:
        return wrapper
    return wrapper(__fn)


@overload
def on_pre_checkout_query(
    __fn: HandlerFunc[PreCheckoutQuery]
) -> Handler[PreCheckoutQuery]:
    ...


@overload
def on_pre_checkout_query(
    *,
    filters: Sequence[Filter[PreCheckoutQuery]] | None = None,
    middleware: Sequence[Middleware[PreCheckoutQuery]] | None = None,
    sort_filters: bool = True,
    any_filter: bool = False,
) -> Wrapper[PreCheckoutQuery]:
    ...


def on_pre_checkout_query(
    __fn: HandlerFunc[PreCheckoutQuery] | None = None,
    *,
    filters: Sequence[Filter[PreCheckoutQuery]] | None = None,
    middleware: Sequence[Middleware[PreCheckoutQuery]] | None = None,
    sort_filters: bool = True,
    any_filter: bool = False,
) -> Wrapper[PreCheckoutQuery] | Handler[PreCheckoutQuery]:
    """Pre-checkout query handler decorator.

    Use this decorator to decorate handler for `pre_checkout_query` update.

    See :class:`Handler` for parameters.
    """

    def wrapper(fn: HandlerFunc[PreCheckoutQuery]) -> Handler[PreCheckoutQuery]:
        handler: Handler[PreCheckoutQuery] = Handler(
            fn=fn,
            update_type=UpdateType.PRE_CHECKOUT_QUERY,
            filters=filters,
            middleware=middleware,
            sort_filters=sort_filters,
            any_filter=any_filter,
        )
        return handler

    if __fn is None:
        return wrapper
    return wrapper(__fn)


@overload
def on_poll(__fn: HandlerFunc[Poll]) -> Handler[Poll]:
    ...


@overload
def on_poll(
    *,
    filters: Sequence[Filter[Poll]] | None = None,
    middleware: Sequence[Middleware[Poll]] | None = None,
    sort_filters: bool = True,
    any_filter: bool = False,
) -> Wrapper[Poll]:
    ...


def on_poll(
    __fn: HandlerFunc[Poll] | None = None,
    *,
    filters: Sequence[Filter[Poll]] | None = None,
    middleware: Sequence[Middleware[Poll]] | None = None,
    sort_filters: bool = True,
    any_filter: bool = False,
) -> Wrapper[Poll] | Handler[Poll]:
    """Poll handler decorator.

    Use this decorator to decorate handler for `poll` update.

    See :class:`Handler` for parameters.
    """

    def wrapper(fn: HandlerFunc[Poll]) -> Handler[Poll]:
        handler: Handler[Poll] = Handler(
            fn=fn,
            update_type=UpdateType.POLL,
            filters=filters,
            middleware=middleware,
            sort_filters=sort_filters,
            any_filter=any_filter,
        )
        return handler

    if __fn is None:
        return wrapper
    return wrapper(__fn)


@overload
def on_poll_answer(__fn: HandlerFunc[PollAnswer]) -> Handler[PollAnswer]:
    ...


@overload
def on_poll_answer(
    *,
    filters: Sequence[Filter[PollAnswer]] | None = None,
    middleware: Sequence[Middleware[PollAnswer]] | None = None,
    sort_filters: bool = True,
    any_filter: bool = False,
) -> Wrapper[PollAnswer]:
    ...


def on_poll_answer(
    __fn: HandlerFunc[PollAnswer] | None = None,
    *,
    filters: Sequence[Filter[PollAnswer]] | None = None,
    middleware: Sequence[Middleware[PollAnswer]] | None = None,
    sort_filters: bool = True,
    any_filter: bool = False,
) -> Wrapper[PollAnswer] | Handler[PollAnswer]:
    """Poll answer handler decorator.

    Use this decorator to decorate handler for `poll_answer` update.

    See :class:`Handler` for parameters.
    """

    def wrapper(fn: HandlerFunc[PollAnswer]) -> Handler[PollAnswer]:
        handler: Handler[PollAnswer] = Handler(
            fn=fn,
            update_type=UpdateType.POLL_ANSWER,
            filters=filters,
            middleware=middleware,
            sort_filters=sort_filters,
            any_filter=any_filter,
        )
        return handler

    if __fn is None:
        return wrapper
    return wrapper(__fn)


@overload
def on_my_chat_member(
    __fn: HandlerFunc[ChatMemberUpdated]
) -> Handler[ChatMemberUpdated]:
    ...


@overload
def on_my_chat_member(
    *,
    filters: Sequence[Filter[ChatMemberUpdated]] | None = None,
    middleware: Sequence[Middleware[ChatMemberUpdated]] | None = None,
    sort_filters: bool = True,
    any_filter: bool = False,
) -> Wrapper[ChatMemberUpdated]:
    ...


def on_my_chat_member(
    __fn: HandlerFunc[ChatMemberUpdated] | None = None,
    *,
    filters: Sequence[Filter[ChatMemberUpdated]] | None = None,
    middleware: Sequence[Middleware[ChatMemberUpdated]] | None = None,
    sort_filters: bool = True,
    any_filter: bool = False,
) -> Wrapper[ChatMemberUpdated] | Handler[ChatMemberUpdated]:
    """My chat member handler decorator.

    Use this decorator to decorate handler for `my_chat_member` update.

    See :class:`Handler` for parameters.
    """

    def wrapper(
        fn: HandlerFunc[ChatMemberUpdated]
    ) -> Handler[ChatMemberUpdated]:
        handler: Handler[ChatMemberUpdated] = Handler(
            fn=fn,
            update_type=UpdateType.MY_CHAT_MEMBER,
            filters=filters,
            middleware=middleware,
            sort_filters=sort_filters,
            any_filter=any_filter,
        )
        return handler

    if __fn is None:
        return wrapper
    return wrapper(__fn)


@overload
def on_chat_member(
    __fn: HandlerFunc[ChatMemberUpdated]
) -> Handler[ChatMemberUpdated]:
    ...


@overload
def on_chat_member(
    *,
    filters: Sequence[Filter[ChatMemberUpdated]] | None = None,
    middleware: Sequence[Middleware[ChatMemberUpdated]] | None = None,
    sort_filters: bool = True,
    any_filter: bool = False,
) -> Wrapper[ChatMemberUpdated]:
    ...


def on_chat_member(
    __fn: HandlerFunc[ChatMemberUpdated] | None = None,
    *,
    filters: Sequence[Filter[ChatMemberUpdated]] | None = None,
    middleware: Sequence[Middleware[ChatMemberUpdated]] | None = None,
    sort_filters: bool = True,
    any_filter: bool = False,
) -> Wrapper[ChatMemberUpdated] | Handler[ChatMemberUpdated]:
    """Chat member handler decorator.

    Use this decorator to decorate handler for `chat_member` update.

    See :class:`Handler` for parameters.
    """

    def wrapper(
        fn: HandlerFunc[ChatMemberUpdated]
    ) -> Handler[ChatMemberUpdated]:
        handler: Handler[ChatMemberUpdated] = Handler(
            fn=fn,
            update_type=UpdateType.CHAT_MEMBER,
            filters=filters,
            middleware=middleware,
            sort_filters=sort_filters,
            any_filter=any_filter,
        )
        return handler

    if __fn is None:
        return wrapper
    return wrapper(__fn)


@overload
def on_chat_join_request(
    __fn: HandlerFunc[ChatJoinRequest]
) -> Handler[ChatJoinRequest]:
    ...


@overload
def on_chat_join_request(
    *,
    filters: Sequence[Filter[ChatJoinRequest]] | None = None,
    middleware: Sequence[Middleware[ChatJoinRequest]] | None = None,
    sort_filters: bool = True,
    any_filter: bool = False,
) -> Wrapper[ChatJoinRequest]:
    ...


def on_chat_join_request(
    __fn: HandlerFunc[ChatJoinRequest] | None = None,
    *,
    filters: Sequence[Filter[ChatJoinRequest]] | None = None,
    middleware: Sequence[Middleware[ChatJoinRequest]] | None = None,
    sort_filters: bool = True,
    any_filter: bool = False,
) -> Wrapper[ChatJoinRequest] | Handler[ChatJoinRequest]:
    """Chat join request handler decorator.

    Use this decorator to decorate handler for `chat_join_request` update.

    See :class:`Handler` for parameters.
    """

    def wrapper(fn: HandlerFunc[ChatJoinRequest]) -> Handler[ChatJoinRequest]:
        handler: Handler[ChatJoinRequest] = Handler(
            fn=fn,
            update_type=UpdateType.CHAT_JOIN_REQUEST,
            filters=filters,
            middleware=middleware,
            sort_filters=sort_filters,
            any_filter=any_filter,
        )
        return handler

    if __fn is None:
        return wrapper
    return wrapper(__fn)
