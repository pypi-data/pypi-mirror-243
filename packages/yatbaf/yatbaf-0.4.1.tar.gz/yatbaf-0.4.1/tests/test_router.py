import unittest.mock as mock
from contextlib import asynccontextmanager

import pytest

from yatbaf.dispatcher import Dispatcher
from yatbaf.enums import UpdateType
from yatbaf.filters import Channel
from yatbaf.filters import Command
from yatbaf.filters import Content
from yatbaf.filters import User
from yatbaf.handler import Handler
from yatbaf.router import OnCallbackQuery
from yatbaf.router import OnChannelPost
from yatbaf.router import OnChatJoinRequest
from yatbaf.router import OnChatMemeber
from yatbaf.router import OnChosenInlineResult
from yatbaf.router import OnEditedChannelPost
from yatbaf.router import OnEditedMessage
from yatbaf.router import OnInlineQuery
from yatbaf.router import OnMessage
from yatbaf.router import OnMyChatMember
from yatbaf.router import OnPoll
from yatbaf.router import OnPollAnswer
from yatbaf.router import OnPreCheckoutQuery
from yatbaf.router import OnShippingQuery


@pytest.fixture
def dispatcher(token):
    return Dispatcher(token)


@pytest.fixture
def router():
    return OnMessage()


@pytest.fixture
def filter():
    return Command("foo")


@pytest.fixture
def handler_func():
    return mock.AsyncMock(return_value=None)


@pytest.fixture
def handler(handler_func):
    return Handler(handler_func, UpdateType.MESSAGE)


def test_update_type():
    assert OnCallbackQuery._update_type == UpdateType.CALLBACK_QUERY
    assert OnChannelPost._update_type == UpdateType.CHANNEL_POST
    assert OnChatJoinRequest._update_type == UpdateType.CHAT_JOIN_REQUEST
    assert OnChatMemeber._update_type == UpdateType.CHAT_MEMBER
    assert OnChosenInlineResult._update_type == UpdateType.CHOSEN_INLINE_RESULT
    assert OnEditedChannelPost._update_type == UpdateType.EDITED_CHANNEL_POST
    assert OnEditedMessage._update_type == UpdateType.EDITED_MESSAGE
    assert OnInlineQuery._update_type == UpdateType.INLINE_QUERY
    assert OnMessage._update_type == UpdateType.MESSAGE
    assert OnMyChatMember._update_type == UpdateType.MY_CHAT_MEMBER
    assert OnPoll._update_type == UpdateType.POLL
    assert OnPollAnswer._update_type == UpdateType.POLL_ANSWER
    assert OnPreCheckoutQuery._update_type == UpdateType.PRE_CHECKOUT_QUERY
    assert OnShippingQuery._update_type == UpdateType.SHIPPING_QUERY


def test_new_router():
    router = OnMessage()
    assert not router._handlers
    assert not router._middleware
    assert not router._guards


def test_add_handler(router, handler_func):
    router.add_handler(handler_func)
    assert isinstance(router._handlers[0], Handler)
    assert router._handlers[0]._fn is handler_func


def test_add_handler_obj(router, handler_func):
    handler = Handler(handler_func, UpdateType.MESSAGE)
    router.add_handler(handler)
    assert router._handlers[0] is handler


def test_add_handler_type_error(router, handler_func):
    handler = Handler(handler_func, UpdateType.POLL)
    with pytest.raises(ValueError):
        router.add_handler(handler)


def test_add_handler_duplicate_func(router, handler_func, filter):
    handler1 = Handler(handler_func, UpdateType.MESSAGE)
    handler2 = Handler(handler_func, UpdateType.MESSAGE, filters=[filter])
    router.add_handler(handler1)
    router.add_handler(handler2)
    assert len(router._handlers) == 1
    assert handler1 in router._handlers
    assert handler2 not in router._handlers


def test_add_handler_duplicate_func1(router, handler_func, filter):
    handler1 = Handler(handler_func, UpdateType.MESSAGE)
    router.add_handler(handler1)
    router.add_handler(handler_func, filters=[filter])
    assert len(router._handlers) == 1
    assert handler1 in router._handlers


def test_add_handler_duplicate_func2(router, handler_func, filter):
    router.add_handler(handler_func)
    router.add_handler(handler_func, filters=[filter])
    assert len(router._handlers) == 1
    assert not router._handlers[0]._filters


def test_add_handler_decorator(router):

    @router
    async def handler(_):  # noqa: U101
        pass

    assert isinstance(router._handlers[0], Handler)
    assert router._handlers[0]._fn is handler


def test_add_handler_decorator_duplicate(router):

    @router
    @router
    async def handler(_):  # noqa: U101
        pass

    assert isinstance(router._handlers[0], Handler)
    assert len(router._handlers) == 1
    assert router._handlers[0]._fn is handler


def test_handler_decorator_filter(router):
    filter = Command("foo")

    @router(filters=[filter])
    async def handler(_):  # noqa: U101
        pass

    assert isinstance(router._handlers[0], Handler)
    assert router._handlers[0]._fn is handler
    assert filter in router._handlers[0]._filters


def test_handler_decorator_middleware(router):
    middleware = mock.Mock()

    @router(middleware=[middleware])
    async def handler(_):  # noqa: U101
        pass

    assert isinstance(router._handlers[0], Handler)
    assert router._handlers[0]._fn is handler
    assert middleware in router._handlers[0]._middleware


def test_handler_decorator_middleware_filter_mix(router, filter):
    middleware = mock.Mock()

    @router(
        middleware=[middleware],
        filters=[filter],
    )
    async def handler(_) -> None:  # noqa: U101
        pass

    assert isinstance(router._handlers[0], Handler)
    assert router._handlers[0]._fn is handler
    assert middleware in router._handlers[0]._middleware
    assert filter in router._handlers[0]._filters


def test_router_init_guard():
    func = object()
    router = OnMessage(guards=[func])
    assert func in router._guards


def test_router_add_guard():
    router = OnMessage()
    func = object()
    router.add_guard(func)
    assert len(router._guards) == 1
    assert func in router._guards


def test_router_add_guard_duplicate():
    router = OnMessage()
    func = object()

    router.add_guard(func)
    router.add_guard(func)
    assert len(router._guards) == 1
    assert func in router._guards


def test_router_guard_decorator(router):

    @router.guard
    async def func(_):  # noqa: U101
        pass

    assert len(router._guards) == 1
    assert func in router._guards


def test_router_init_middleware():
    func = object()
    router = OnMessage(middleware=[func])
    assert func in router._middleware


def test_router_add_middleware(router):
    func = object()
    router.add_middleware(func)
    assert func in router._middleware


def test_router_middleware_decorator(router):

    @router.middleware
    def func(_):  # noqa: U101
        pass

    assert len(router._middleware) == 1
    assert func in router._middleware


def test_router_middleware_decorator_duplicate(router):

    @router.middleware
    @router.middleware
    def func(_):  # noqa: U101
        pass

    assert len(router._middleware) == 1
    assert func in router._middleware


def test_find_handler_none_no_handlers(router, message):
    assert router._find_handler(message) is None


def test_find_handler_no_filters(router, message, handler):
    router.add_handler(handler)
    assert router._find_handler(message) is handler


def test_find_handler_catch_all(handler, router, message, asyncdef, filter):
    router.add_handler(handler)
    router.add_handler(asyncdef(), filters=[filter])
    message.text = "/bar"
    assert router._find_handler(message) is handler


def test_find_handler_filter(router, message, asyncdef, filter, handler_func):
    router.add_handler(asyncdef())
    handler = Handler(handler_func, UpdateType.MESSAGE, filters=[filter])
    router.add_handler(handler)
    message.text = "/foo"
    assert router._find_handler(message) is handler


def test_add_router():
    router = OnMessage()
    nested = OnMessage()
    router.add_router(nested)
    assert len(router._routers) == 1
    assert nested in router._routers


def test_add_router_self(router):
    with pytest.raises(ValueError):
        router.add_router(router)


def test_add_router_wrong_type(router):
    with pytest.raises(ValueError):
        router.add_router(OnPoll())


def test_add_router_dispatcher(router, dispatcher):
    with pytest.raises(RuntimeError):
        router.add_router(dispatcher)


def test_add_router_duplicate():
    router = OnMessage()
    nested = OnMessage()
    router.add_router(nested)
    router.add_router(nested)
    assert len(router._routers) == 1
    assert nested in router._routers


@pytest.mark.asyncio
async def test_resolve_no_handlers(router, update_info):
    router._on_registration()
    assert not await router._resolve(update_info)


@pytest.mark.asyncio
async def test_resolve_catch_all(router, update_info, handler_func):
    router.add_handler(handler_func)
    router._on_registration()
    assert await router._resolve(update_info)
    handler_func.assert_awaited_once()


@pytest.mark.asyncio
async def test_resolve_none(router, update_info, handler_func):
    filter = Command("foo")
    router.add_handler(handler_func, filters=[filter])
    router._on_registration()
    assert not await router._resolve(update_info)
    handler_func.assert_not_awaited()


@pytest.mark.asyncio
async def test_resolve_nested_vert(update_info, handler_func):

    def find_router(router):
        r = router
        while r._routers:
            r = r._routers[-1]
        return r

    router = OnMessage()
    for _ in range(5):
        find_router(router).add_router(OnMessage())

    filter = Command("foo")
    update_info.content.text = "/foo"
    find_router(router).add_handler(handler_func, filters=[filter])
    router._on_registration()
    assert await router._resolve(update_info)
    handler_func.assert_awaited_once()


@pytest.mark.asyncio
async def test_resolve_nested_horiz(update_info, handler_func):
    router = OnMessage()
    for _ in range(5):
        router.add_router(OnMessage())
    filter = Command("foo")
    update_info.content.text = "/foo"
    router._routers[-1].add_handler(handler_func, filters=[filter])
    router._on_registration()
    assert await router._resolve(update_info)
    handler_func.assert_awaited_once()


@pytest.mark.asyncio
async def test_guard_false(handler_func, router, update_info, asyncdef):
    router.add_guard(asyncdef(False))
    router.add_handler(handler_func)
    router._on_registration()
    assert not await router._resolve(update_info)
    handler_func.assert_not_awaited()


@pytest.mark.asyncio
async def test_guard_true(handler_func, router, update_info, asyncdef):
    router.add_guard(asyncdef(True))
    router.add_handler(handler_func)
    router._on_registration()
    assert await router._resolve(update_info)
    handler_func.assert_awaited_once()


@pytest.mark.asyncio
async def test_parent_guard_true(handler_func, update_info, asyncdef):
    router = OnMessage()
    router.add_guard(asyncdef(True))
    router.add_handler(handler_func)

    router1 = OnMessage()
    router1.add_handler(asyncdef())

    router.add_router(router1)
    router._on_registration()
    assert await router._resolve(update_info)
    handler_func.assert_awaited_once()


@pytest.mark.asyncio
async def test_parent_guard_false(handler_func, update_info, asyncdef):
    router = OnMessage()
    router.add_guard(asyncdef(False))
    router.add_handler(asyncdef())

    router1 = OnMessage()
    router1.add_handler(handler_func)

    router.add_router(router1)
    router._on_registration()
    assert await router._resolve(update_info)
    handler_func.assert_awaited_once()


@pytest.mark.asyncio
async def test_guard_false_both(handler_func, update_info, asyncdef):
    router = OnMessage()
    router.add_guard(asyncdef(False))
    router.add_handler(asyncdef())

    router1 = OnMessage()
    router1.add_guard(asyncdef(False))
    router1.add_handler(handler_func)

    router.add_router(router1)
    router._on_registration()
    assert not await router._resolve(update_info)
    handler_func.assert_not_awaited()


@pytest.mark.asyncio
async def test_guard_skip_nested(handler_func, update_info, asyncdef):
    router = OnMessage(skip_with_nested=True)
    router.add_guard(asyncdef(False))

    router1 = OnMessage()
    router1.add_guard(asyncdef(True))
    router1.add_handler(handler_func)

    router.add_router(router1)
    assert not await router._resolve(update_info)
    handler_func.assert_not_awaited()


@pytest.fixture
def middleware_factory():
    # yapf: disable
    def factory(mark):
        def middleware(handler):
            async def wrapper(update):
                mark()
                await handler(update)
            return wrapper
        return middleware
    return factory
    # yapf: enable


@pytest.mark.asyncio
async def test_resolve_wrap_router_middlewares(
    router, update_info, handler_func, middleware_factory
):
    m = mock.Mock()
    router.add_handler(handler_func)
    for _ in range(5):
        router.add_middleware(middleware_factory(m))
    assert len(router._middleware) == 5

    router._on_registration()
    assert await router._resolve(update_info)
    handler_func.assert_awaited_once_with(update_info.content)
    assert m.call_count == 5


@pytest.mark.asyncio
async def test_resolve_wrap_handler_middlewares(
    router, handler_func, update_info, middleware_factory
):
    m = mock.Mock()
    router.add_handler(
        handler_func,
        middleware=[middleware_factory(m) for _ in range(5)],
    )
    router._on_registration()
    assert await router._resolve(update_info)
    assert m.call_count == 5
    handler_func.assert_awaited_once_with(update_info.content)


@pytest.mark.asyncio
async def test_resolve_wrap_middlewares(
    router, middleware_factory, update_info, handler_func
):
    m = mock.Mock()
    router.add_handler(
        handler_func,
        middleware=[middleware_factory(m) for _ in range(5)],
    )
    for _ in range(5):
        router.add_middleware(middleware_factory(m))
    router._on_registration()
    assert await router._resolve(update_info)
    assert m.call_count == 10
    handler_func.assert_awaited_once_with(update_info.content)


@pytest.mark.asyncio
async def test_router_context(update_info):

    @asynccontextmanager
    async def ctx(m):
        m.ctx["foo"] = "bar"
        yield
        del m.ctx["foo"]

    async def handler(m):
        m.ctx["foo"]

    router = OnMessage(context=ctx)
    router.add_handler(handler)
    router._on_registration()
    await router._resolve(update_info)


@pytest.mark.asyncio
async def test_router_context_nested(update_info):

    @asynccontextmanager
    async def ctx(m):
        m.ctx["foo"] = "bar"
        yield
        del m.ctx["foo"]

    async def handler(m):
        m.ctx["foo"]

    router = OnMessage(context=ctx)
    tmp = router
    for _ in range(5):
        r = OnMessage()
        tmp.add_router(r)
        tmp = r
    tmp.add_handler(handler)
    router._on_registration()
    await router._resolve(update_info)


@pytest.mark.asyncio
async def test_router_context_nested_(update_info):
    keys = list(range(0, 5))

    def ctx_factory(key):

        @asynccontextmanager
        async def ctx(m):
            m.ctx[key] = key
            yield
            del m.ctx[key]

        return ctx

    async def handler(m):
        for k in keys:
            m.ctx[k]

    router = OnMessage(context=ctx_factory(keys[0]))
    tmp = router
    for k in keys[1:]:
        r = OnMessage(context=ctx_factory(k))
        tmp.add_router(r)
        tmp = r
    tmp.add_handler(handler)
    router._on_registration()
    await router._resolve(update_info)


def test_sort_filters_router_true():
    user = User(123)
    channel = Channel()
    command = Command("start")
    content = Content("text")

    router = OnMessage()
    router.add_handler(
        object(), filters=[
            content,
            command,
            user,
            channel,
        ]
    )
    assert router._handlers[0]._filters == [channel, user, content, command]


def test_sort_filters_router_true_func_false():
    user = User(123)
    channel = Channel()
    command = Command("start")
    content = Content("text")

    router = OnMessage()
    router.add_handler(
        object(),
        filters=[
            content,
            command,
            user,
            channel,
        ],
        sort_filters=False,
    )
    assert router._handlers[0]._filters == [content, command, user, channel]


def test_sort_filters_router_false():
    user = User(123)
    channel = Channel()
    command = Command("start")
    content = Content("text")

    router = OnMessage(sort_filters=False)
    router.add_handler(
        object(), filters=[
            content,
            command,
            user,
            channel,
        ]
    )
    assert router._handlers[0]._filters == [content, command, user, channel]


def test_sort_filters_router_false_func_true():
    user = User(123)
    channel = Channel()
    command = Command("start")
    content = Content("text")

    router = OnMessage(sort_filters=False)
    router.add_handler(
        object(),
        filters=[
            content,
            command,
            user,
            channel,
        ],
        sort_filters=True,
    )
    assert router._handlers[0]._filters == [channel, user, content, command]
