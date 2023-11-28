from __future__ import annotations

__all__ = ("Text",)

from re import compile as re_compile
from typing import TYPE_CHECKING
from typing import final

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Iterable
    from re import Pattern

    from yatbaf.types import Message


@final
class Text:
    """Message text filter.

    See :class:`yatbaf.filters.content.Content`.

    Use it to filter message by text content::

        @on_message(filters=[Text(match="foo bar")])
        async def handler(message: Message) -> None:
            assert message.text == "foo bar"


        @on_message(filters=[Text(startswith="foo")])
        async def handler(message: Message) -> None:
            assert message.text.startswith("foo")


        @on_message(
            filters=[
                Text(
                    startswith="foo",
                    endswith="bar",
                    contains="baz",
                )
            ]
        )
        async def handler(message: Message) -> None:
            assert (
                (t := message.text).startswith("foo")
                and t.endswith("bar")
                and "baz" in t
            )

    """

    __slots__ = (
        "priority",
        "params",
        "ignore_case",
        "any_",
    )

    def __init__(
        self,
        startswith: str | None = None,
        endswith: str | None = None,
        match: str | None = None,
        contains: str | Iterable[str] | None = None,
        regexp: str | Pattern | None = None,
        any_: bool = False,
        ignore_case: bool = False,
        priority: int = 300,  # same as Content filter
    ) -> None:
        """
        :param startswith: *Optional.* Text prefix.
        :param endswith: *Optional.* Text suffix.
        :param match: *Optional.* Check if text is equal to passed string.
        :param contains: *Optional.* A string or list of strings to check if
            it is in the message.
        :param regexp: *Optional.* Regular expression.
        :param any_: Pass ``True``, if one match is enough. Default ``False``.
        :param ignore_case: Perform case-insensitive matching.
            Default ``False``.
        :param priority: Filter priority. Default 300.
        :raise ValueError: If all optional parameters is ``None``.

        .. note::

            You **must** pass at least one optional parameter, otherwise
            ``ValueError`` is raised.

        """
        params: list[Callable[[str], bool]] = []
        if startswith is not None:
            params.append(
                lambda s: s.startswith(startswith)  # type: ignore[arg-type]
            )

        if endswith is not None:
            params.append(
                lambda s: s.endswith(endswith)  # type: ignore[arg-type]
            )

        if match is not None:
            params.append(lambda s: s == match)

        if contains is not None:
            if isinstance(contains, str):
                contains = (contains,)
            # yapf: disable
            params.append(
                lambda s: any(w in s for w in contains)  # type: ignore[union-attr]  # noqa: E501
            )
            # yapf: enable

        if regexp is not None:
            if isinstance(regexp, str | bytes):
                regexp = re_compile(regexp)
            # re.search returns re.Match or None, re.Match is always True.
            params.append(regexp.search)  # type: ignore[arg-type]

        if not params:
            raise ValueError(
                "No parameters. "
                "You must pass at least one optional parameter."
            )

        self.ignore_case = ignore_case
        self.params = params
        self.priority = priority
        self.any_ = any_

    def check(self, update: Message) -> bool:
        # same behavior as Content(TEXT) filter
        if (text := update.text) is None:
            return False

        f = any if self.any_ else all
        text = text.lower() if self.ignore_case else text
        return f(p(text) for p in self.params)
