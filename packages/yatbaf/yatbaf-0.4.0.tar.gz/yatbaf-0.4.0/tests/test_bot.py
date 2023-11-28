import unittest.mock as mock

import msgspec
import pytest

from yatbaf import Bot
from yatbaf import OnMessage
from yatbaf import on_message
from yatbaf.filters import Command


@pytest.mark.asyncio
async def test_bot(token, update):
    mark = mock.Mock()

    @on_message(filters=[Command("foo")])
    async def handler(message):
        mark(message)

    bot = Bot(token, handlers=[handler])

    update.message.text = "/foo"
    await bot.process_update(update)

    mark.assert_called_once_with(update.message)


@pytest.mark.asyncio
async def test_bot_webhook(token, update):
    mark = mock.Mock()

    @on_message(filters=[Command("foo")])
    async def handler(message):
        mark(message)

    bot = Bot(token, handlers=[handler])

    update.message.text = "/foo"
    webhook_content = msgspec.json.encode(update)
    await bot.process_update(webhook_content)

    mark.assert_called_once_with(update.message)


@pytest.mark.asyncio
async def test_bot_frozen(token):
    router = OnMessage()
    _ = Bot(token, routers=[router])

    with pytest.raises(RuntimeError):

        @router.guard
        async def g(_):
            pass

    with pytest.raises(RuntimeError):

        @router.middleware
        def m(_):
            pass

    with pytest.raises(RuntimeError):

        @router
        async def h(_):
            pass
