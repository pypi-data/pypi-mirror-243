import time
import unittest.mock as mock

import pytest

from yatbaf.models import UpdateInfo
from yatbaf.router import OnMessage
from yatbaf.types import Chat
from yatbaf.types import Message
from yatbaf.types import Update
from yatbaf.types import User


@pytest.fixture
def token():
    return "12345678:testtoken"


@pytest.fixture
def handler():
    return mock.AsyncMock(return_value=None)


@pytest.fixture
def user():
    return User(
        id=1010,
        username="testuser",
        is_bot=False,
        first_name="Test",
    )


@pytest.fixture
def chat():
    return Chat(
        id=101010,
        type="group",
        username="testchat",
    )


@pytest.fixture
def message(chat, user):
    return Message(
        from_=user,
        chat=chat,
        date=int(time.time()),
        message_id=101010,
    )


@pytest.fixture
def update(message):
    return Update(
        update_id=9999,
        message=message,
    )


@pytest.fixture
def update_info(update):
    return UpdateInfo(
        id=update.update_id,
        content=update.message,
        name="message",
    )


@pytest.fixture
def router():
    return OnMessage()


# yapf: disable
@pytest.fixture
def asyncdef():
    def factory(result=None):
        async def func(*_, **__):  # noqa: U101
            return result
        return func
    return factory
    # yapf: enable
