from __future__ import annotations

__all__ = (
    "OnMessage",
    "OnEditedMessage",
    "OnChannelPost",
    "OnEditedChannelPost",
    "OnInlineQuery",
    "OnChosenInlineResult",
    "OnCallbackQuery",
    "OnShippingQuery",
    "OnPreCheckoutQuery",
    "OnPoll",
    "OnPollAnswer",
    "OnMyChatMember",
    "OnChatMemeber",
    "OnChatJoinRequest",
)

import logging
from itertools import count
from typing import TYPE_CHECKING
from typing import Any
from typing import Final
from typing import Generic
from typing import Literal
from typing import Self
from typing import TypeAlias
from typing import TypeVar
from typing import final
from typing import overload

from .abc import AbstractRouter
from .handler import Handler
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
from .typing import UpdateT
from .utils import ensure_unique

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Sequence

    from .models import UpdateInfo
    from .typing import Context
    from .typing import Filter
    from .typing import Guard
    from .typing import HandlerFunc
    from .typing import Middleware

log = logging.getLogger(__name__)
_router_count = count(1).__next__

T = TypeVar("T")
Wrapper: TypeAlias = "Callable[[HandlerFunc[T]], HandlerFunc[T]]"


class _EmptyContext(Generic[UpdateT]):

    async def __aenter__(self) -> None:
        pass

    async def __aexit__(self, *exc_info: Any) -> None:  # noqa: U100
        pass

    def __call__(self, update: UpdateT) -> Self:  # noqa: U100
        return self


_empty_context: Context[Any] = _EmptyContext()


class BaseRouter(AbstractRouter[UpdateT]):
    """Common behaviour for :class:`Router` and
    :class:`~yatbaf.dispatcher.Dispatcher`.
    """

    __slots__ = (
        "_context",
        "_guards",
        "_middleware",
        "_parent",
    )

    def __init__(
        self,
        guards: Sequence[Guard[UpdateT]] | None = None,
        middleware: Sequence[Middleware[UpdateT]] | None = None,
        routers: Sequence[AbstractRouter[UpdateT]] | None = None,
        handlers: Sequence[Handler[UpdateT]] | None = None,
        context: Context[UpdateT] | None = None,
    ) -> None:
        """
        :param guards: *Optional.* A sequence of :class:`~yatbaf.typing.Guard`.
        :param middleware: *Optional.* A sequence of :class:`~yatbaf.typing.Middleware`.
        :param routers: *Optional.* A sequence of :class:`~yatbaf.abc.AbstractRouter`.
        :param handlers: *Optional.* A sequence of :class:`~yatbaf.typing.Handler`.
        :param context: *Optional.* Router :class:`~yatbaf.typing.Context`.
        """  # noqa: E501
        self._context = _empty_context if context is None else context
        self._guards: list[Guard[UpdateT]] = ensure_unique(guards or [])
        self._middleware = ensure_unique(middleware or [])
        self._parent = None

        self._register_routers(routers or [])
        self._register_handlers(handlers or [])

    async def _check_guards(self, update: UpdateT) -> bool:
        for func in self._guards:
            if not await func(update):
                return False
        return True


class Router(BaseRouter[UpdateT]):
    """Base class for routers."""

    __slots__ = (
        "_routers",
        "_sort_filters",
        "_skip_with_nested",
        "_update_type",
        "_handlers",
        "_name",
        "_frozen",
    )

    def __init__(
        self,
        *,
        handlers: Sequence[Handler[UpdateT]] | None = None,
        middleware: Sequence[Middleware[UpdateT]] | None = None,
        routers: Sequence[AbstractRouter[UpdateT]] | None = None,
        guards: Sequence[Guard[UpdateT]] | None = None,
        name: str | None = None,
        sort_filters: bool = True,
        skip_with_nested: bool = False,
        context: Context[UpdateT] | None = None,
    ) -> None:
        """
        :param handlers: *Optional.* A sequence of :class:`~yatbaf.typing.Handler`.
        :param middleware: *Optional.* A sequence of :class:`~yatbaf.typing.Middleware`.
        :param routers: *Optional.* A sequence of :class:`~yatbaf.abc.AbstractRouter`.
        :param guards: *Optional.* A sequence of :class:`~yatbaf.typing.Guard`.
        :param name: *Optional.* Router name.
        :param sort_filters: *Optional.* Sort handler filters by priority.
        :param skip_with_nested: *Optional.* Guard will also skip nested routers.
        :param context: *Optional.* Router :class:`~yatbaf.typing.Context`.
        """  # noqa: E501
        self._sort_filters: Final[bool] = sort_filters
        self._skip_with_nested: Final[bool] = skip_with_nested
        self._routers: list[AbstractRouter[UpdateT]] = []
        self._handlers: list[Handler[UpdateT]] = []
        self._name: Final[str] = name if name else f"router-{_router_count()}"
        self._frozen = False

        super().__init__(
            routers=routers,
            handlers=handlers,
            guards=guards,
            middleware=middleware,
            context=context,
        )

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}[name={self._name}]>"

    @property
    def name(self) -> str:
        """Router name."""
        return self._name

    def _register_routers(
        self, routers: Sequence[AbstractRouter[UpdateT]]
    ) -> None:
        for router in routers:
            self.add_router(router)

    def _register_handlers(self, handlers: Sequence[Handler[UpdateT]]) -> None:
        for handler in handlers:
            self.add_handler(handler)

    def add_guard(self, func: Guard[UpdateT], /) -> None:
        """Add a new guard function.

        :param func: :class:`Guard <yatbaf.typing.Guard>` function.
        :raises RuntimeError: If you try to register a Guard after Bot object
            has been initialized.
        """
        if self._frozen:
            raise RuntimeError(
                "It is not possible to add a new Guard at runtime "
                "after Bot object has been initialized."
            )

        if func not in self._guards:
            self._guards.append(func)

    def add_middleware(self, func: Middleware[UpdateT], /) -> None:
        """Add a new middleware.

        Add a new middleware which will be applied to all handlers in router.
        Function must return a new Handler functoin. Usage::

            def middleware(handler: Handler) -> Handler:
                async def wrapper(update: UpdateT) -> None:
                    await handler(update)
                return wrapper

            router.add_middleware(middleware)

        :param func: :class:`Middleware <yatbaf.types.Middleware>` function.
        :raises RuntimeError: If you try to register a Middleware after Bot
            object has been initialized.
        """
        if self._frozen:
            raise RuntimeError(
                "It is not possible to add a new Middleware at runtime "
                "after Bot object has been initialized."
            )

        # skip duplicate
        if func not in self._middleware:
            self._middleware.append(func)

    @overload
    def add_handler(self, handler: Handler[UpdateT]) -> None:
        ...

    @overload
    def add_handler(
        self,
        handler: HandlerFunc[UpdateT],
        *,
        filters: Sequence[Filter[UpdateT]] | None = None,
        middleware: Sequence[Middleware[UpdateT]] | None = None,
        sort_filters: bool | None = None,
        any_filter: bool = False,
    ) -> None:
        ...

    def add_handler(
        self,
        handler: HandlerFunc[UpdateT] | Handler[UpdateT],
        *,
        filters: Sequence[Filter[UpdateT]] | None = None,
        middleware: Sequence[Middleware[UpdateT]] | None = None,
        sort_filters: bool | None = None,
        any_filter: bool = False,
    ) -> None:
        """Use this method to register a new handler.

        :param handler: :class:`~yatbaf.handler.Handler` instance or function.
        :param filters: *Optional.* A sequence of :class:`~yatbaf.typing.Filter`.
        :param middleware: *Optional.* A sequence of :class:`~yatbaf.typing.Middleware`.
        :param sort_filters: *Optional.* Pass ``False`` if you want to use your
            filter order. Default to :attr:`Router.sort_filters`.
        :param any_filter: Pass ``True`` if matching one of the filters is enough.
        :raises RuntimeError: If you try to register a Handler after Bot object
            has been initialized.
        """  # noqa: E501
        if self._frozen:
            raise RuntimeError(
                f"{self!r} is frozen. It is not possible to add a new Handler "
                "at runtime after Bot object has been initialized."
            )

        if isinstance(handler, Handler):
            if handler.update_type != self._update_type:
                raise ValueError(
                    f"Type mismatch! You can't add {handler!r} to {self!r}"
                )

            if handler._parent is not None and handler._parent is not self:
                raise ValueError(
                    f"{handler!r} alredy registered in {handler._parent!r}"
                )

        else:
            handler = Handler(
                fn=handler,
                update_type=self._update_type,
                filters=filters,
                middleware=middleware,
                sort_filters=(
                    self._sort_filters if sort_filters is None else sort_filters
                ),
                any_filter=any_filter,
            )

        # skip duplicate
        for obj in self._handlers:
            if obj._fn is handler._fn:
                return

        handler._parent = self
        self._handlers.append(handler)

    @overload
    def __call__(self, __fn: HandlerFunc[UpdateT]) -> HandlerFunc[UpdateT]:
        ...

    @overload
    def __call__(
        self,
        *,
        filters: Sequence[Filter[UpdateT]] | None = None,
        middleware: Sequence[Middleware[UpdateT]] | None = None,
        sort_filters: bool | None = None,
        any_filter: bool = False,
    ) -> Wrapper[UpdateT]:
        ...

    def __call__(
        self,
        __fn: HandlerFunc[UpdateT] | None = None,
        *,
        filters: Sequence[Filter[UpdateT]] | None = None,
        middleware: Sequence[Middleware[UpdateT]] | None = None,
        sort_filters: bool | None = None,
        any_filter: bool = False,
    ) -> Wrapper[UpdateT] | HandlerFunc[UpdateT]:
        """Handler decorator.

        See :meth:`add_handler`.

        Use this decorator to register a new handler::

            @router
            async def handler(update):
                ...

            @router(filters=[filter1, filter2])
            async def handler(update):
                ...
        """

        def wrapper(fn: HandlerFunc[UpdateT]) -> HandlerFunc[UpdateT]:
            self.add_handler(
                handler=fn,
                filters=filters,
                middleware=middleware,
                sort_filters=sort_filters,
                any_filter=any_filter,
            )
            return fn

        if __fn is not None:
            return wrapper(__fn)
        return wrapper

    def add_router(self, router: AbstractRouter[UpdateT], /) -> None:
        """Use this method to add a nested router.

        .. warning::

            The nested router must handle the same type of updates as the
            current one.

        :param router: :class:`~yatbaf.abc.AbstractRouter` instance.
        :raises ValueError: If ``router`` already registered in another router.
        :raises ValueError: If ``router`` update type is different.
        :raises RuntimeError: If you try to register a Router after Bot object
            has been initialized.
        """
        if self._frozen:
            raise RuntimeError(
                f"{self!r} is frozen. It is not possible to add a new Router "
                "at runtime after Bot object has been initialized."
            )

        if router is self:
            raise ValueError("self to self? i call the police!")
        if self._update_type != router._update_type:
            raise ValueError(
                "Type mismatch. "
                f"Cannot add {router._update_type!r} to {self._update_type!r}"
            )
        if router._parent is None:
            router._parent = self
            self._routers.append(router)
        elif router._parent is not self:
            raise ValueError(
                f"{router!r} already registered in {router._parent!r}"
            )

    def _find_handler(self, update: UpdateT) -> Handler[UpdateT] | None:
        result: Handler[UpdateT] | None = None
        for handler in self._handlers:
            if handler._match(update):
                if not handler._is_fallback():
                    return handler
                result = handler
        return result

    async def _resolve(self, update: UpdateInfo[UpdateT], /) -> bool:
        content = update.content
        async with self._context(content):
            if await self._check_guards(content):
                if (handler := self._find_handler(content)) is not None:
                    await handler(content)
                    return True

            # guard failed
            elif self._skip_with_nested:
                return False

            # try to find the handler in nested routers
            for router in self._routers:
                if await router._resolve(update):
                    return True

        return False

    def middleware(self, fn: Middleware[UpdateT], /) -> Middleware[UpdateT]:
        """Middleware decorator.

        Use this decorator to register a middleware for router::

            @router.middleware
            def middleware(handler):
                async def wrapper(update):
                    await handler(update)
                return wrapper
        """
        self.add_middleware(fn)
        return fn

    def guard(self, fn: Guard[UpdateT], /) -> Guard[UpdateT]:
        """Guard decorator.

        Use this decorator to register a guard for router::

            @router.guard
            async def guard(update):
                return True
        """
        self.add_guard(fn)
        return fn

    def _on_registration(self) -> None:
        self._frozen = True
        for handler in self._handlers:
            handler._on_registration()
        for router in self._routers:
            router._on_registration()


@final
class OnMessage(Router[Message]):
    """message router.

    See :attr:`Update.message <yatbaf.types.update.Update.message>`
    """

    __slots__ = ()
    _update_type: Literal["message"] = "message"


@final
class OnEditedMessage(Router[Message]):
    """edited_message router.

    See :attr:`Update.edited_message <yatbaf.types.update.Update.edited_message>`
    """  # noqa: E501

    __slots__ = ()
    _update_type: Literal["edited_message"] = "edited_message"


@final
class OnChannelPost(Router[Message]):
    """channel_post router.

    See :attr:`Update.channel_post <yatbaf.types.update.Update.channel_post>`
    """

    __slots__ = ()
    _update_type: Literal["channel_post"] = "channel_post"


@final
class OnEditedChannelPost(Router[Message]):
    """edited_channel_post router.

    See :attr:`Update.edited_channel_post <yatbaf.types.update.Update.edited_channel_post>`
    """  # noqa: E501

    __slots__ = ()
    _update_type: Literal["edited_channel_post"] = "edited_channel_post"


@final
class OnInlineQuery(Router[InlineQuery]):
    """inline_query router.

    See :attr:`Update.inline_query <yatbaf.types.update.Update.inline_query>`
    """

    __slots__ = ()
    _update_type: Literal["inline_query"] = "inline_query"


@final
class OnChosenInlineResult(Router[ChosenInlineResult]):
    """chosen_inline_result router.

    See :attr:`Update.chosen_inline_result <yatbaf.types.update.Update.chosen_inline_result>`
    """  # noqa: E501

    __slots__ = ()
    _update_type: Literal["chosen_inline_result"] = "chosen_inline_result"


@final
class OnCallbackQuery(Router[CallbackQuery]):
    """callback_query router.

    See :attr:`Update.callback_query <yatbaf.types.update.Update.callback_query>`
    """  # noqa: E501

    __slots__ = ()
    _update_type: Literal["callback_query"] = "callback_query"


@final
class OnShippingQuery(Router[ShippingQuery]):
    """shipping_query router.

    See :attr:`Update.shipping_query <yatbaf.types.update.Update.shipping_query>`
    """  # noqa: E501

    __slots__ = ()
    _update_type: Literal["shipping_query"] = "shipping_query"


@final
class OnPreCheckoutQuery(Router[PreCheckoutQuery]):
    """pre_checkout_query router.

    See :attr:`Update.pre_checkout_query <yatbaf.types.update.Update.pre_checkout_query>`
    """  # noqa: E501

    __slots__ = ()
    _update_type: Literal["pre_checkout_query"] = "pre_checkout_query"


@final
class OnPoll(Router[Poll]):
    """poll router.

    See :attr:`Update.poll <yatbaf.types.update.Update.poll>`
    """

    __slots__ = ()
    _update_type: Literal["poll"] = "poll"


@final
class OnPollAnswer(Router[PollAnswer]):
    """poll_answer router.

    See :attr:`Update.poll_answer <yatbaf.types.update.Update.poll_answer>`
    """

    __slots__ = ()
    _update_type: Literal["poll_answer"] = "poll_answer"


@final
class OnMyChatMember(Router[ChatMemberUpdated]):
    """my_chat_member router.

    See :attr:`Update.my_chat_member <yatbaf.types.update.Update.my_chat_member>`
    """  # noqa: E501

    __slots__ = ()
    _update_type: Literal["my_chat_member"] = "my_chat_member"


@final
class OnChatMemeber(Router[ChatMemberUpdated]):
    """chat_member router.

    See :attr:`Update.chat_member <yatbaf.types.update.Update.chat_member>`
    """

    __slots__ = ()
    _update_type: Literal["chat_member"] = "chat_member"


@final
class OnChatJoinRequest(Router[ChatJoinRequest]):
    """chat_join_request router.

    See :attr:`Update.chat_join_request <yatbaf.types.update.Update.chat_join_request>`
    """  # noqa: E501

    __slots__ = ()
    _update_type: Literal["chat_join_request"] = "chat_join_request"


router_map: dict[str, type[BaseRouter]] = {
    "message": OnMessage,
    "edited_message": OnEditedMessage,
    "channel_post": OnChannelPost,
    "edited_channel_post": OnEditedChannelPost,
    "inline_query": OnInlineQuery,
    "chosen_inline_result": OnChosenInlineResult,
    "callback_query": OnCallbackQuery,
    "shipping_query": OnShippingQuery,
    "pre_checkout_query": OnPreCheckoutQuery,
    "poll": OnPoll,
    "poll_answer": OnPollAnswer,
    "my_chat_member": OnMyChatMember,
    "chat_member": OnChatMemeber,
    "chat_join_request": OnChatJoinRequest,
}
