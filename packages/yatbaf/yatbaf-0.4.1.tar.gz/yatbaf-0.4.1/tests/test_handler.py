import unittest.mock as mock

import pytest

from yatbaf.enums import UpdateType
from yatbaf.filters import Chat
from yatbaf.filters import Command
from yatbaf.filters import User
from yatbaf.handler import Handler
from yatbaf.router import OnMessage


def test_new_hander(handler):
    h = Handler(handler, update_type=UpdateType.MESSAGE)
    assert not h._filters
    assert not h._middleware
    assert h._update_type is UpdateType.MESSAGE
    assert str(h) == "<Handler[type=message]>"
    assert h._match_fn is all


def test_filter(handler):
    cmd_filter = Command("cmd")
    chat_filter = Chat()
    h = Handler(
        handler,
        update_type=UpdateType.MESSAGE,
        filters=[cmd_filter, chat_filter],
    )
    assert len(h._filters) == 2
    assert h._filters[0] is chat_filter
    assert h._filters[1] is cmd_filter


def test_filter_sort_false(handler):
    cmd_filter = Command("cmd")
    chat_filter = Chat()
    h = Handler(
        handler,
        update_type=UpdateType.MESSAGE,
        filters=[cmd_filter, chat_filter],
        sort_filters=False,
    )
    assert len(h._filters) == 2
    assert h._filters[0] is cmd_filter
    assert h._filters[1] is chat_filter


def test_middleware(handler):
    middleware = mock.Mock()
    h = Handler(
        handler,
        update_type=UpdateType.MESSAGE,
        middleware=[middleware],
    )
    assert middleware in h._middleware


def test_wrap_middlewares(handler):
    middleware = mock.Mock(return_value=(func := mock.AsyncMock()))
    h = Handler(
        handler,
        update_type=UpdateType.MESSAGE,
        middleware=[middleware],
    )
    assert h._build_middleware_stack() is func


def test_wrap_middlewares_empty(handler):
    h = Handler(
        handler,
        update_type=UpdateType.MESSAGE,
    )
    assert h._build_middleware_stack() is handler


def test_wrap_middleware_order(handler):
    middleware1 = mock.Mock(return_value=(func1 := mock.AsyncMock()))
    middleware2 = mock.Mock()
    middleware3 = mock.Mock()
    h = Handler(
        handler,
        update_type=UpdateType.MESSAGE,
        middleware=[
            middleware1,
            middleware2,
            middleware3,
        ],
    )
    assert h._build_middleware_stack() is func1


def test_wrap_middleware_parent(handler):
    middleware1 = mock.Mock(return_value=(func1 := mock.AsyncMock()))
    middleware2 = mock.Mock()
    middleware3 = mock.Mock()
    h = Handler(
        handler,
        update_type=UpdateType.MESSAGE,
        middleware=[
            middleware2,
            middleware3,
        ],
    )
    _ = OnMessage(
        middleware=[middleware1],
        handlers=[h],
    )
    assert h._build_middleware_stack() is func1


def test_match_empty_true(handler, message):
    h = Handler(
        handler,
        update_type=UpdateType.MESSAGE,
    )
    assert h._match(message)


def test_is_fallback(handler):
    h = Handler(
        handler,
        update_type=UpdateType.MESSAGE,
        filters=[Command("foo")],
    )
    assert not h._is_fallback()


def test_empty_is_fallback(handler):
    h = Handler(
        handler,
        update_type=UpdateType.MESSAGE,
    )
    assert h._is_fallback()


def test_match_true(handler, message):
    message.text = "/foo"
    h = Handler(
        handler,
        update_type=UpdateType.MESSAGE,
        filters=[Command("foo")],
    )
    assert h._match(message)


def test_match_true1(handler, message):
    message.text = "/foo"
    h = Handler(
        handler,
        update_type=UpdateType.MESSAGE,
        filters=[
            Command("foo"),
            User(message.from_.id),
        ]
    )
    assert h._match(message)


def test_match_false(handler, message):
    message.text = "/bar"
    h = Handler(
        handler,
        update_type=UpdateType.MESSAGE,
        filters=[Command("foo")],
    )
    assert not h._match(message)


def test_match_false1(handler, message):
    message.text = "/foo"
    h = Handler(
        handler,
        update_type=UpdateType.MESSAGE,
        filters=[
            Command("bar"),
            User(1),
        ],
    )
    assert not h._match(message)


@pytest.mark.asyncio
async def test_orig_func(handler, message):
    h = Handler(
        handler,
        update_type=UpdateType.MESSAGE,
    )
    await h.orig(message)
    handler.assert_awaited_once_with(message)
