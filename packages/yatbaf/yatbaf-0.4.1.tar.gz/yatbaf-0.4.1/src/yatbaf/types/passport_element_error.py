from __future__ import annotations

__all__ = (
    "PassportElementError",
    "PassportElementErrorDataField",
    "PassportElementErrorFile",
    "PassportElementErrorFiles",
    "PassportElementErrorFrontSide",
    "PassportElementErrorReverseSide",
    "PassportElementErrorSelfie",
    "PassportElementErrorTranslationFile",
    "PassportElementErrorTranslationFiles",
    "PassportElementErrorUnspecified",
)

from typing import TYPE_CHECKING
from typing import Literal
from typing import TypeAlias
from typing import final

from msgspec import field

if TYPE_CHECKING:
    from yatbaf.enums import PassportElement

from .abc import TelegramType


@final
class PassportElementErrorFile(TelegramType):
    """Represents an issue with a document scan. The error is considered
    resolved when the file with the document scan changes.

    See: https://core.telegram.org/bots/api#passportelementerrorfile
    """

    type: PassportElement
    """The section of the user's Telegram Passport which has the issue."""

    file_hash: str
    """Base64-encoded file hash."""

    message: str
    """Error message"""

    source: Literal["file"] = field(default_factory=lambda: "file")
    """Error source, must be `file`."""


@final
class PassportElementErrorFiles(TelegramType):
    """Represents an issue with a list of scans. The error is considered
    resolved when the list of files containing the scans changes.

    See: https://core.telegram.org/bots/api#passportelementerrorfiles
    """

    type: PassportElement
    """The section of the user's Telegram Passport which has the issue."""

    file_hashes: list[str]
    """List of base64-encoded file hashes."""

    message: str
    """Error message."""

    source: Literal["files"] = field(default_factory=lambda: "files")
    """Error source, must be `files`."""


@final
class PassportElementErrorSelfie(TelegramType):
    """Represents an issue with the selfie with a document. The error is
    considered resolved when the file with the selfie changes.

    # https://core.telegram.org/bots/api#passportelementerrorselfie
    """

    type: PassportElement
    """The section of the user's Telegram Passport which has the issue."""

    file_hash: str
    """Base64-encoded hash of the file with the selfie."""

    message: str
    """Error message."""

    source: Literal["selfie"] = field(default_factory=lambda: "selfie")
    """Error source, must be `selfie`."""


@final
class PassportElementErrorFrontSide(TelegramType):
    """Represents an issue with the front side of a document. The error is
    considered resolved when the file with the front side of the document
    changes.

    See: https://core.telegram.org/bots/api#passportelementerrorfrontside
    """

    type: PassportElement
    """The section of the user's Telegram Passport which has the issue."""

    file_hash: str
    """Base64-encoded hash of the file with the front side of the document."""

    message: str
    """Error message."""

    source: Literal["front_side"] = field(default_factory=lambda: "front_side")
    """Error source, must be `front_side`."""


@final
class PassportElementErrorUnspecified(TelegramType):
    """Represents an issue in an unspecified place. The error is considered
    resolved when new data is added.

    See: https://core.telegram.org/bots/api#passportelementerrorunspecified
    """

    type: PassportElement
    """Type of element of the user's Telegram Passport which has the issue."""

    element_hash: str
    """Base64-encoded element hash."""

    message: str
    """Error message."""

    source: Literal["unspecified"] = field(
        default_factory=lambda: "unspecified"
    )
    """Error source, must be `unspecified`."""


@final
class PassportElementErrorReverseSide(TelegramType):
    """Represents an issue with the reverse side of a document. The error is
    considered resolved when the file with reverse side of the document changes.

    See: https://core.telegram.org/bots/api#passportelementerrorreverseside
    """

    type: PassportElement
    """The section of the user's Telegram Passport which has the issue."""

    file_hash: str
    """Base64-encoded hash of the file with the reverse side of the document."""

    message: str
    """Error message."""

    source: Literal["reverse_side"] = field(
        default_factory=lambda: "reverse_side"
    )
    """Error source, must be `reverse_side`."""


@final
class PassportElementErrorTranslationFile(TelegramType):
    """Represents an issue with one of the files that constitute the translation
    of a document. The error is considered resolved when the file changes.

    See: https://core.telegram.org/bots/api#passportelementerrortranslationfile
    """

    type: PassportElement
    """ype of element of the user's Telegram Passport which has the issue."""

    file_hash: str
    """Base64-encoded file hash."""

    message: str
    """Error message."""

    source: Literal["translation_file"] = field(
        default_factory=lambda: "translation_file"
    )
    """Error source, must be `translation_file`."""


@final
class PassportElementErrorTranslationFiles(TelegramType):
    """Represents an issue with the translated version of a document. The error
    is considered resolved when a file with the document translation change.

    See: https://core.telegram.org/bots/api#passportelementerrortranslationfiles
    """

    type: PassportElement
    """Type of element of the user's Telegram Passport which has the issue."""

    file_hashes: list[str]
    """List of base64-encoded file hashes."""

    message: str
    """Error message."""

    source: Literal["translation_files"] = field(
        default_factory=lambda: "translation_files"
    )
    """Error source, must be `translation_files`."""


@final
class PassportElementErrorDataField(TelegramType):
    """Represents an issue in one of the data fields that was provided by the
    user. The error is considered resolved when the field's value changes.

    See: https://core.telegram.org/bots/api#passportelementerrordatafield
    """

    type: PassportElement
    """The section of the user's Telegram Passport which has the error."""

    field_name: str
    """Name of the data field which has the error."""

    data_hash: str
    """Base64-encoded data hash."""

    message: str
    """Error message"""

    source: Literal["data"] = field(default_factory=lambda: "data")
    """Error source, must be `data`."""


# https://core.telegram.org/bots/api#passportelementerror
# Represents an error in the Telegram Passport element which was submitted that
# should be resolved by the user.
PassportElementError: TypeAlias = (
    "PassportElementErrorDataField "
    "| PassportElementErrorFile "
    "| PassportElementErrorFiles "
    "| PassportElementErrorFrontSide "
    "| PassportElementErrorReverseSide "
    "| PassportElementErrorSelfie "
    "| PassportElementErrorTranslationFile "
    "| PassportElementErrorTranslationFiles "
    "| PassportElementErrorUnspecified"
)
