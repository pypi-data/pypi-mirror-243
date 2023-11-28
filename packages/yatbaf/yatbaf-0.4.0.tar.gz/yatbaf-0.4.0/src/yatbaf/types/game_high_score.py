from __future__ import annotations

from typing import final

from .abc import TelegramType
from .user import User


@final
class GameHighScore(TelegramType):
    """This object represents one row of the high scores table for a game.

    See: https://core.telegram.org/bots/api#gamehighscore
    """

    position: int
    """Position in high score table for the game."""

    user: User
    """User."""

    score: int
    """Score."""
