import unittest.mock as mock
from contextlib import asynccontextmanager

import pytest

from yatbaf.dispatcher import Dispatcher
from yatbaf.enums import UpdateType
from yatbaf.handler import Handler
from yatbaf.models import UpdateInfo
from yatbaf.router import OnEditedChannelPost
from yatbaf.router import OnEditedMessage
from yatbaf.router import OnMessage
from yatbaf.router import OnPoll


def test_routers(token):
    dispatcher = Dispatcher(token)
    for type_ in UpdateType:
        dispatcher._routers[type_]


def test_dispatcher(token):
    dispatcher = Dispatcher(token)
    assert dispatcher._routers
    assert not dispatcher._middleware
    assert not dispatcher._guards


def test_add_router(token, router):
    dispatcher = Dispatcher(token, routers=[router])
    assert len(routers := dispatcher._routers[router._update_type]) == 1
    assert router in routers


def test_add_router_duplicate(token):
    router = OnMessage()
    dispatcher = Dispatcher(token, routers=[router, router])
    assert len(routers := dispatcher._routers[router._update_type]) == 1
    assert router in routers


def test_add_routers(token):
    dispatcher = Dispatcher(
        token,
        routers=[
            message := OnMessage(),
            poll := OnPoll(),
            edited_message := OnEditedMessage(),
            edited_post := OnEditedChannelPost(),
        ],
    )
    assert message in dispatcher._routers["message"]
    assert poll in dispatcher._routers["poll"]
    assert edited_message in dispatcher._routers["edited_message"]
    assert edited_post in dispatcher._routers["edited_channel_post"]


def test_dispatcher_update_type(token):
    with pytest.raises(RuntimeError):
        Dispatcher(token)._update_type


@pytest.mark.asyncio
async def test_resolve_no_routers(token, update_info):
    dispatcher = Dispatcher(token)
    assert not await dispatcher._resolve(update_info)


@pytest.mark.asyncio
async def test_resolve(token, handler, update_info):
    dispatcher = Dispatcher(
        token,
        routers=[OnMessage(handlers=[handler])],
    )
    await dispatcher._resolve(update_info)
    handler.assert_awaited_once_with(update_info.content)


@pytest.mark.asyncio
async def test_resolve_none(token, handler, update_info):
    dispatcher = Dispatcher(token, routers=[OnPoll(handlers=[handler])])
    await dispatcher._resolve(update_info)
    handler.assert_not_awaited()


@pytest.mark.asyncio
async def test_resolve_guard_false(token, handler, update_info, asyncdef):
    dispatcher = Dispatcher(
        token,
        guards=[asyncdef(False)],
        routers=[OnMessage(handlers=[handler])]
    )
    await dispatcher._resolve(update_info)
    handler.assert_not_awaited()


@pytest.mark.asyncio
async def test_resolve_guard_true(token, handler, update_info, asyncdef):
    dispatcher = Dispatcher(
        token,
        guards=[asyncdef(True)],
        routers=[OnMessage(handlers=[handler])],
    )
    await dispatcher._resolve(update_info)
    handler.assert_awaited_once_with(update_info.content)


@pytest.mark.asyncio
async def test_process_update(monkeypatch, token, update):
    monkeypatch.setattr(Dispatcher, "_bind_self", lambda _, v: v)
    monkeypatch.setattr(
        Dispatcher, "_resolve", resolve := mock.AsyncMock(return_value=None)
    )
    dispatcher = Dispatcher(token)
    await dispatcher.process_update(update)
    resolve.assert_awaited_once_with(
        UpdateInfo(
            id=update.update_id,
            content=update.message,
            name="message",
        )
    )


@pytest.mark.asyncio
async def test_context(token, update_info):
    router = OnMessage()

    @router
    async def handler(u):
        u.ctx["test"]

    @asynccontextmanager
    async def context(u):
        u.ctx["test"] = 1
        yield
        del u.ctx["test"]

    dispatcher = Dispatcher(token, context=context, routers=[router])
    await dispatcher._resolve(update_info)


def test_add_handler_duplicate(token, handler):
    dispatcher = Dispatcher(
        token,
        handlers=[
            Handler(handler, UpdateType.MESSAGE),
            Handler(handler, UpdateType.MESSAGE),
        ],
    )
    assert dispatcher._routers["message"]
    assert len(dispatcher._routers["message"]) == 1


def test_add_handler_order(token):
    dispatcher = Dispatcher(
        token,
        handlers=[
            h1 := Handler(object(), UpdateType.MESSAGE),
            h3 := Handler(object(), UpdateType.MESSAGE),
            h2 := Handler(object(), UpdateType.MESSAGE),
        ]
    )
    assert len(dispatcher._routers["message"]) == 1
    assert len(dispatcher._routers["message"][-1]._handlers) == 3
    assert dispatcher._routers["message"][-1]._handlers[0] is h1
    assert dispatcher._routers["message"][-1]._handlers[1] is h3
    assert dispatcher._routers["message"][-1]._handlers[2] is h2


def test_add_handler_message(token, handler):
    dispatcher = Dispatcher(
        token,
        handlers=[
            h := Handler(handler, UpdateType.MESSAGE),
        ],
    )
    assert dispatcher._routers["message"][-1]._handlers[0] is h


def test_add_handler_edited_message(token, handler):
    dispatcher = Dispatcher(
        token,
        handlers=[
            h := Handler(handler, UpdateType.EDITED_MESSAGE),
        ],
    )
    assert dispatcher._routers["edited_message"][-1]._handlers[0] is h


def test_add_handler_channel_post(token, handler):
    dispatcher = Dispatcher(
        token,
        handlers=[
            h := Handler(handler, UpdateType.CHANNEL_POST),
        ],
    )
    assert dispatcher._routers["channel_post"][-1]._handlers[0] is h


def test_add_handler_edited_channel_post(token, handler):
    dispatcher = Dispatcher(
        token,
        handlers=[
            h := Handler(handler, UpdateType.EDITED_CHANNEL_POST),
        ],
    )
    assert dispatcher._routers["edited_channel_post"][-1]._handlers[0] is h


def test_add_handler_inline_query(token, handler):
    dispatcher = Dispatcher(
        token,
        handlers=[
            h := Handler(handler, UpdateType.INLINE_QUERY),
        ],
    )
    assert dispatcher._routers["inline_query"][-1]._handlers[0] is h


def test_add_handler_chosen_inline_result(token, handler):
    dispatcher = Dispatcher(
        token,
        handlers=[
            h := Handler(handler, UpdateType.CHOSEN_INLINE_RESULT),
        ],
    )
    assert dispatcher._routers["chosen_inline_result"][-1]._handlers[0] is h


def test_add_handler_callback_query(token, handler):
    dispatcher = Dispatcher(
        token,
        handlers=[
            h := Handler(handler, UpdateType.CALLBACK_QUERY),
        ],
    )
    assert dispatcher._routers["callback_query"][-1]._handlers[0] is h


def test_add_handler_shipping_query(token, handler):
    dispatcher = Dispatcher(
        token,
        handlers=[
            h := Handler(handler, UpdateType.SHIPPING_QUERY),
        ],
    )
    assert dispatcher._routers["shipping_query"][-1]._handlers[0] is h


def test_add_handler_pre_checkout_query(token, handler):
    dispatcher = Dispatcher(
        token,
        handlers=[
            h := Handler(handler, UpdateType.PRE_CHECKOUT_QUERY),
        ],
    )
    assert dispatcher._routers["pre_checkout_query"][-1]._handlers[0] is h


def test_add_handler_poll(token, handler):
    dispatcher = Dispatcher(
        token,
        handlers=[
            h := Handler(handler, UpdateType.POLL),
        ],
    )
    assert dispatcher._routers["poll"][-1]._handlers[0] is h


def test_add_handler_poll_answer(token, handler):
    dispatcher = Dispatcher(
        token,
        handlers=[
            h := Handler(handler, UpdateType.POLL_ANSWER),
        ],
    )
    assert dispatcher._routers["poll_answer"][-1]._handlers[0] is h


def test_add_handler_my_chat_member(token, handler):
    dispatcher = Dispatcher(
        token,
        handlers=[
            h := Handler(handler, UpdateType.MY_CHAT_MEMBER),
        ],
    )
    assert dispatcher._routers["my_chat_member"][-1]._handlers[0] is h


def test_add_handler_chat_member(token, handler):
    dispatcher = Dispatcher(
        token,
        handlers=[
            h := Handler(handler, UpdateType.CHAT_MEMBER),
        ],
    )
    assert dispatcher._routers["chat_member"][-1]._handlers[0] is h


def test_add_handler_chat_join_request(token, handler):
    dispatcher = Dispatcher(
        token,
        handlers=[
            h := Handler(handler, UpdateType.CHAT_JOIN_REQUEST),
        ],
    )
    assert dispatcher._routers["chat_join_request"][-1]._handlers[0] is h
