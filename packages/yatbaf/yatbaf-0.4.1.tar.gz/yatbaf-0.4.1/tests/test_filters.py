import re
import unittest.mock as mock

import pytest

from yatbaf.enums import ChatType
from yatbaf.enums import ContentType
from yatbaf.filters import And
from yatbaf.filters import Channel
from yatbaf.filters import Command
from yatbaf.filters import Content
from yatbaf.filters import Group
from yatbaf.filters import Not
from yatbaf.filters import Or
from yatbaf.filters import Text
from yatbaf.filters import User

USER_ID = 34567
CHAT_ID = 9876


@pytest.fixture
def update_message():
    update = mock.MagicMock()
    update.from_.id = USER_ID
    update.from_.username = "test_user"
    update.chat.id = CHAT_ID
    return update


class FalseFilter:
    priority = 100

    def check(self, _):  # noqa: U101
        return False


class TrueFilter:
    priority = 100

    def check(self, _):  # noqa: U101
        return True


def test_filter_not_true(update_message):
    assert Not(FalseFilter()).check(update_message)


def test_filter_not_false(update_message):
    assert not Not(TrueFilter()).check(update_message)


def test_filter_or_true(update_message):
    assert Or(FalseFilter(), TrueFilter()).check(update_message)


def test_filter_or_false(update_message):
    assert not Or(FalseFilter(), FalseFilter()).check(update_message)


def test_filter_and_true(update_message):
    assert And(TrueFilter(), TrueFilter()).check(update_message)


def test_filter_and_false(update_message):
    assert not And(TrueFilter(), FalseFilter()).check(update_message)


@pytest.mark.parametrize("user", ("@test_user", "test_user", USER_ID))
def test_filter_user(update_message, user):
    assert User(user).check(update_message)


@pytest.mark.parametrize("user", ("@testuser", "test_user1", 23345678))
def test_filter_not_user(update_message, user):
    assert not User(user).check(update_message)


@pytest.mark.parametrize("user", ("@test_user", "test_user", USER_ID))
def test_filter_invert_user(update_message, user):
    assert not Not(User(user)).check(update_message)


@pytest.mark.parametrize("t", (ChatType.GROUP, ChatType.SUPERGROUP))
def test_filter_group(update_message, t):
    update_message.chat.type = t
    assert Group().check(update_message)


@pytest.mark.parametrize("t", (ChatType.GROUP, ChatType.SUPERGROUP))
def test_filter_group_ids(update_message, t):
    update_message.chat.type = t
    assert Group(CHAT_ID).check(update_message)
    assert not Group(123).check(update_message)


def test_filter_channel(update_message):
    update_message.chat.type = ChatType.CHANNEL
    assert Channel().check(update_message)


def test_filter_channel_ids(update_message):
    update_message.chat.type = ChatType.CHANNEL
    assert Channel(CHAT_ID).check(update_message)
    assert not Channel(123).check(update_message)


def test_filter_content_empty():
    with pytest.raises(ValueError):
        Content()


def test_filter_content_wrong_type():
    with pytest.raises(ValueError):
        Content("typo")


def test_filter_content_true(update_message):
    update_message.text = "123"
    assert Content("text").check(update_message)
    assert Content(ContentType.TEXT).check(update_message)


def test_filter_content_false(update_message):
    update_message.text = "123"
    update_message.document = None
    assert not Content("document").check(update_message)
    assert not Content(ContentType.DOCUMENT).check(update_message)


def test_filter_command_empty():
    with pytest.raises(ValueError):
        Command()


def test_filter_command_true(update_message):
    update_message.text = "/start"
    assert Command("start").check(update_message)
    assert Command("/start").check(update_message)
    assert Command("START").check(update_message)
    assert Command("Start").check(update_message)
    assert Command("hello", "start").check(update_message)


def test_filter_command_false(update_message):
    update_message.text = "/pong"
    assert not Command("ping").check(update_message)


def test_filter_command_text_is_none(update_message):
    update_message.text = None
    assert not Command("ping").check(update_message)


def test_filter_text_no_params():
    with pytest.raises(ValueError):
        Text()


def test_filter_text_is_text(update_message):
    update_message.text = None
    assert not Text(startswith="foo").check(update_message)


@pytest.mark.parametrize("f,ic", (("FOO", False), ("foo", True)))
def test_filter_text_start(update_message, f, ic):
    update_message.text = "FOO bar"
    assert Text(startswith=f, ignore_case=ic).check(update_message)


@pytest.mark.parametrize("f,ic", (("BAR", False), ("bar", True)))
def test_filter_text_end(update_message, f, ic):
    update_message.text = "foo BAR"
    assert Text(endswith=f, ignore_case=ic).check(update_message)


def test_filter_text_start_end(update_message):
    update_message.text = "foo baz bar"
    assert Text(startswith="foo", endswith="bar").check(update_message)


def test_filter_text_start_end_any(update_message):
    update_message.text = "foo bar baz"
    assert (
        Text(startswith="foo", endswith="bar", any_=True).check(update_message)
    )


@pytest.mark.parametrize("m,ic", (("Foo Bar", False), ("foo bar", True)))
def test_filter_text_match(update_message, m, ic):
    update_message.text = "Foo Bar"
    assert Text(match=m, ignore_case=ic).check(update_message)


def test_filter_text_match_false(update_message):
    update_message.text = "foo bar"
    assert not Text(match="foo b").check(update_message)


@pytest.mark.parametrize("c", ("bar", ["oof", "foo"]))
def test_filter_text_contains(update_message, c):
    update_message.text = "foo bar baz"
    assert Text(contains=c).check(update_message)


def test_filter_text_contains_false(update_message):
    update_message.text = "foo bar baz"
    assert not Text(contains="foobar").check(update_message)


@pytest.mark.parametrize("t", ("foobarbaz", "foo bar baz"))
def test_filter_text_start_end_contains(update_message, t):
    update_message.text = t
    assert Text(
        startswith="fo",
        endswith="az",
        contains="bar",
    ).check(update_message)


@pytest.mark.parametrize("exp", (".+baz.*$", re.compile("^f.+az$")))
def test_filter_text_regexp(update_message, exp):
    update_message.text = "foo bar baz"
    assert Text(regexp=exp).check(update_message)


def test_priority():
    user = User(123)
    channel = Channel()
    command = Command("start")
    content = Content("text")

    assert Not(channel).priority == channel.priority
    assert And(command, user).priority == user.priority
    assert Or(channel, content).priority == channel.priority
