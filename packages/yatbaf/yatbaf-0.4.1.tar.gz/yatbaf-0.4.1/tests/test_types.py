import pytest


def test_attr_is_private(message):
    assert "__usrctx__" not in message.__struct_fields__
    assert "__usrctx__" not in message.__slots__


def test_ctx_empty(message):
    assert not message.ctx


def test_ctx(message):
    message.ctx["foo"] = "bar"
    assert "foo" in message.__usrctx__


def test_bind_bot_obj(message):
    bot = object()
    message._bind_bot_obj(bot)
    assert message.bot is bot
    assert message.from_.bot is bot
    assert message.chat.bot is bot


def test_bot_not_bound(message):
    with pytest.raises(RuntimeError):
        message.bot
