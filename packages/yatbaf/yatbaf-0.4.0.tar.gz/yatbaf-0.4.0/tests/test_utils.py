import pytest

from yatbaf.utils import parse_command


@pytest.mark.parametrize(
    "text,result",
    (
        ("/foo", "foo"),
        ("/foo@bot", "foo"),
        ("/foo bar 123", "foo"),
        ("/foo@bot bar 123", "foo"),
        ("/FoO@bot bar 123", "foo"),
    )
)
def test_parse_command(text, result):
    assert (r := parse_command(text)) == result, r


@pytest.mark.parametrize(
    "text", ("foo", "foo@bot", "foo bar 123", "foo@bot bar 123", "/")
)
def test_parse_command_none(text):
    assert parse_command(text) is None
