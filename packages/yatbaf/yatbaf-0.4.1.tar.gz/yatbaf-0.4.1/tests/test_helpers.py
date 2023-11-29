import pytest

from yatbaf.enums import AdminFlag
from yatbaf.enums import MarkdownEntity
from yatbaf.helpers import create_bot_deeplink
from yatbaf.helpers import create_channel_deeplink
from yatbaf.helpers import create_game_deeplink
from yatbaf.helpers import create_group_deeplink
from yatbaf.helpers import create_user_link
from yatbaf.helpers import create_webapp_deeplink
from yatbaf.helpers import md
from yatbaf.helpers import parse_command_args


@pytest.mark.parametrize(
    "text,result",
    (
        ("/foo", []),
        ("/foo bar", ["bar"]),
        ("/foo@bot bar baz", ["bar", "baz"]),
        ("/foo Bar baZ 123", ["Bar", "baZ", "123"]),
    ),
)
def test_parse_args(text, result):
    assert parse_command_args(text) == result


@pytest.mark.parametrize(
    "text,expect",
    (
        ("foo", "foo"),
        ("foo.", "foo\\."),
        ("*foo*.", "\\*foo\\*\\."),
        ("_*foo__.", "\\_\\*foo\\_\\_\\."),
        ("__foo__", "\\_\\_foo\\_\\_"),
        ("!foo__.", "\\!foo\\_\\_\\."),
        ("foo != bar", "foo \\!\\= bar"),
        ("foo|bar", "foo\\|bar"),
        ("foo {} bar", "foo \\{\\} bar"),
        ("foo > bar", "foo \\> bar"),
        ("#!/usr/foo/bar -baz", "\\#\\!/usr/foo/bar \\-baz"),
        ("#![!_foo(~bar_)`].", "\\#\\!\\[\\!\\_foo\\(\\~bar\\_\\)\\`\\]\\."),
    )
)
def test_markdown_escape(text, expect):
    assert (result := md.escape(text)) == expect, result


@pytest.mark.parametrize(
    "text,expect", (
        ("foo", "foo"),
        ("foo {}", "foo {}"),
        ("foo {0}", "foo {0}"),
    )
)
def test_markdown_escape_fstring(text, expect):
    assert (result := md.escape(text, MarkdownEntity.FSTRING)) == expect, result
    assert result.format(s := "bar") == expect.format(s)


@pytest.mark.parametrize(
    "text,expect",
    (
        ("foo", "foo"),
        ("`foo`", "\\`foo\\`"),
        ("``\\foo\\``", "\\`\\`\\\\foo\\\\\\`\\`"),
    )
)
def test_markdown_escape_code_pre(text, expect):
    assert md.escape(text, MarkdownEntity.PRE) == expect
    assert md.escape(text, MarkdownEntity.CODE) == expect


@pytest.mark.parametrize(
    "text,expect",
    (
        ("foo", "foo"),
        ("http://foo.bar?q=(\\baz)", "http://foo.bar?q=(\\\\baz\\)"),
        ("http://foo.bar?q=\\))\\!baz", "http://foo.bar?q=\\\\\\)\\)\\\\!baz"),
    )
)
def test_markdown_escape_link_emoji(text, expect):
    assert md.escape(text, MarkdownEntity.LINK) == expect
    assert md.escape(text, MarkdownEntity.EMOJI) == expect


def test_markdown_bold():
    assert md.bold("bold") == "*bold*"


def test_markdown_italic():
    assert md.italic("italic") == "_italic_"


def test_markdown_underline():
    assert md.underline("underline") == "__underline__"


def test_markdown_strikethrough():
    assert md.strikethrough("strikethrough") == "~strikethrough~"


def test_markdown_spoiler():
    assert md.spoiler("spoiler") == "||spoiler||"


def test_markdown_url():
    assert (
        md.url("url title", "https://foo.bar") == "[url title](https://foo.bar)"
    )


def test_markdown_mention():
    assert md.mention("user", 1234) == "[user](tg://user?id=1234)"


def test_markdown_emoji():
    assert md.emoji(1234, "emoji") == "![emoji](tg://emoji?id=1234)"


def test_markdown_inline():
    assert md.inline("foo") == "`foo`"


def test_markdown_code():
    assert md.code("print('foo')") == "```\nprint('foo')\n```"
    assert md.code("print('foo')", "python") == "```python\nprint('foo')\n```"


@pytest.mark.parametrize("username", ("bot123", "user_bot"))
def test_create_user_link(username):
    assert create_user_link(username) == f"https://t.me/{username}"


@pytest.mark.parametrize("username", ("bot-123", "bt", "@bot"))
def test_create_user_link_error(username):
    with pytest.raises(ValueError):
        create_user_link(username)


@pytest.mark.parametrize("parameter", ("123-payload", None))
def test_create_bot_deeplink(parameter):
    bot_username = "username_bot"
    result = create_bot_deeplink(bot_username, parameter)
    if parameter is not None:
        assert result == f"https://t.me/{bot_username}?start={parameter}"
    else:
        assert result == f"https://t.me/{bot_username}"


def test_create_bot_deeplink_parameter_gt64():
    with pytest.raises(ValueError):
        create_bot_deeplink("botusername", "parameter" * 10)


@pytest.mark.parametrize("parameter", (
    "param@",
    "param&",
    ";;;",
    "foo bar",
))
def test_create_bot_deeplink_parameter_invalid_chars(parameter):
    with pytest.raises(ValueError):
        create_bot_deeplink("botusername", parameter)


def test_create_group_deeplink_empty():
    bot = "botusername"
    assert create_group_deeplink(bot) == f"https://t.me/{bot}?startgroup"


def test_create_group_deeplink_parameter():
    bot = "botusername"
    parameter = "parameter_123"
    assert (
        create_group_deeplink(bot, parameter) ==
        f"https://t.me/{bot}?startgroup={parameter}"
    )


def test_create_group_deeplink_parameter_empty():
    bot = "botusername"
    assert create_group_deeplink(bot, "") == f"https://t.me/{bot}?startgroup"


def test_create_group_deeplink_admin():
    bot = "botusername"
    flags = [AdminFlag.CHANGE_INFO, AdminFlag.EDIT_MESSAGES]
    assert (
        create_group_deeplink(bot, admin=flags) ==
        f"https://t.me/{bot}?startgroup&admin=change_info+edit_messages"
    )


def test_create_group_deeplink_admin_empty():
    bot = "botusername"
    assert (
        create_group_deeplink(bot, admin=[]) == f"https://t.me/{bot}?startgroup"
    )


def test_create_group_deeplink_parameter_admin():
    bot = "botusername"
    parameter = "param_foo-bar"
    flags = [
        AdminFlag.EDIT_MESSAGES,
        AdminFlag.INVITE_USERS,
        AdminFlag.DELETE_MESSAGES,
    ]
    assert (
        create_group_deeplink(bot, parameter, flags) == (
            f"https://t.me/{bot}?startgroup={parameter}"
            "&admin=edit_messages+invite_users+delete_messages"
        )
    )


def test_create_group_deeplink_parameter_error():
    with pytest.raises(ValueError):
        create_group_deeplink("botusername", "parameter#")


def test_create_channel_deeplink():
    bot = "botusername"
    flags = [
        AdminFlag.EDIT_MESSAGES,
        AdminFlag.DELETE_MESSAGES,
    ]
    assert (
        create_channel_deeplink(bot, flags) == (
            f"https://t.me/{bot}?startchannel"
            "&admin=edit_messages+delete_messages"
        )
    )


def test_create_channel_deeplink_admin_empty():
    with pytest.raises(ValueError):
        create_channel_deeplink("botusername", [])


def test_create_game_deeplink():
    bot = "botusername"
    game = "gameshortname"
    assert create_game_deeplink(bot, game) == f"https://t.me/{bot}?game={game}"


def test_create_game_deeplink_error():
    with pytest.raises(ValueError):
        create_game_deeplink("invalidbot#", "gameshortname")


def test_create_webapp_deeplink():
    bot = "botusername"
    webapp = "webappname"
    assert (
        create_webapp_deeplink(bot, webapp) ==
        f"https://t.me/{bot}/{webapp}?startapp"
    )


def test_create_webapp_deeplink_parameter():
    bot = "botusername"
    webapp = "webappname"
    parameter = "parameter"
    assert (
        create_webapp_deeplink(bot, webapp, parameter) ==
        f"https://t.me/{bot}/{webapp}?startapp={parameter}"
    )


def test_create_webapp_deeplink_parameter_empty():
    bot = "botusername"
    webapp = "webappname"
    parameter = ""
    assert (
        create_webapp_deeplink(bot, webapp, parameter) ==
        f"https://t.me/{bot}/{webapp}?startapp"
    )


def test_create_webapp_deeplink_parameter_error():
    with pytest.raises(ValueError):
        create_webapp_deeplink("botusername", "webapp", "invalidparam#")
