from __future__ import annotations

__all__ = (
    "EncryptedCredentials",
    "EncryptedPassportElement",
    "PassportFile",
    "PassportData",
)

# from datetime import datetime

from typing import final

from yatbaf.enums import PassportElement
from yatbaf.typing import NoneStr

from .abc import TelegramType


@final
class EncryptedCredentials(TelegramType):
    """Describes data required for decrypting and authenticating :class:`EncryptedPassportElement`.

    See: https://core.telegram.org/bots/api#encryptedcredentials
    """  # noqa: E501

    data: str
    """Base64-encoded encrypted JSON-serialized data with unique user's payload,
    data hashes and secrets required for :class:`EncryptedPassportElement`
    decryption and authentication.
    """

    hash: str
    """Base64-encoded data hash for data authentication."""

    secret: str
    """Base64-encoded secret, encrypted with the bot's public RSA key, required
    for data decryption.
    """


@final
class PassportFile(TelegramType):
    """This object represents a file uploaded to Telegram Passport.

    .. note::

        Currently all Telegram Passport files are in JPEG format when decrypted
        and don't exceed 10MB.

    See: https://core.telegram.org/bots/api#passportfile
    """

    file_id: str
    """
    Identifier for this file, which can be used to download or reuse the file.
    """

    file_unique_id: str
    """Unique identifier for this file, which is supposed to be the same over
    time and for different bots. Can't be used to download or reuse the file.
    """

    file_size: int
    """File size in bytes."""

    file_date: int  # TODO: datetime?
    """Unix time when the file was uploaded."""


@final
class EncryptedPassportElement(TelegramType):
    """Describes documents or other Telegram Passport elements shared with the
    bot by the user.

    See: https://core.telegram.org/bots/api#encryptedpassportelement
    """

    type: PassportElement
    """Element type."""

    hash: str
    """Base64-encoded element hash for using in :class:`~yatbaf.types.passport_element_error.PassportElementErrorUnspecified`."""  # noqa: E501

    data: NoneStr = None
    """*Optional.* Base64-encoded encrypted Telegram Passport element data
    provided by the user, available for “personal_details”, “passport”,
    “driver_license”, “identity_card”, “internal_passport” and “address” types.
    Can be decrypted and verified using the accompanying
    :class:`EncryptedCredentials`.
    """

    phone_number: NoneStr = None
    """*Optional.* User's verified phone number, available only for
    “phone_number” type.
    """

    email: NoneStr = None
    """
    *Optional.* User's verified email address, available only for “email” type.
    """

    files: list[PassportFile] | None = None
    """*Optional.* Array of encrypted files with documents provided by the user,
    available for “utility_bill”, “bank_statement”, “rental_agreement”,
    “passport_registration” and “temporary_registration” types. Files can be
    decrypted and verified using the accompanying :class:`EncryptedCredentials`.
    """

    front_side: PassportFile | None = None
    """*Optional.* Encrypted file with the front side of the document, provided
    by the user. Available for “passport”, “driver_license”, “identity_card”
    and “internal_passport”. The file can be decrypted and verified using the
    accompanying :class:`EncryptedCredentials`.
    """

    reverse_side: PassportFile | None = None
    """*Optional.* Encrypted file with the reverse side of the document,
    provided by the user. Available for “driver_license” and “identity_card”.
    The file can be decrypted and verified using the accompanying
    :class:`EncryptedCredentials`.
    """

    selfie: PassportFile | None = None
    """*Optional.* Encrypted file with the selfie of the user holding a
    document, provided by the user; available for “passport”, “driver_license”,
    “identity_card” and “internal_passport”. The file can be decrypted and
    verified using the accompanying :class:`EncryptedCredentials`.
    """

    translation: list[PassportFile] | None = None
    """*Optional.* Array of encrypted files with translated versions of
    documents provided by the user. Available if requested for “passport”,
    “driver_license”, “identity_card”, “internal_passport”, “utility_bill”,
    “bank_statement”, “rental_agreement”, “passport_registration” and
    “temporary_registration” types. Files can be decrypted and verified using
    the accompanying :class:`EncryptedCredentials`.
    """


@final
class PassportData(TelegramType):
    """Describes Telegram Passport data shared with the bot by the user.

    See: https://core.telegram.org/bots/api#passportdata
    """

    data: list[EncryptedPassportElement]
    """List with information about documents and other Telegram Passport
    elements that was shared with the bot.
    """

    credentials: EncryptedCredentials
    """Encrypted credentials required to decrypt the data."""
