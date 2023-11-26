# -*- coding: utf-8 -*-

"""

qrstu.transcode

Functions to transcode between encodings


Copyright (C) 2023 Rainer Schwarzbach

This file is part of qrstu.

qrstu is free software: you can redistribute it and/or modify
it under the terms of the MIT License.

qrstu is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the LICENSE file for more details.

"""


import codecs
import dataclasses
import io
import pathlib
import shutil

from typing import Any, Dict, IO, List, Union

from qrstu import constants


DEFAULT_TARGET_ENCODING = constants.UTF_8
DEFAULT_FALLBACK_ENCODING = constants.CP1252

# Encodings with byte order marks

BOMS_BY_ENCODING: Dict[str, bytes] = {
    constants.UTF_32_BE: codecs.BOM_UTF32_BE,
    constants.UTF_32_LE: codecs.BOM_UTF32_LE,
    constants.UTF_16_BE: codecs.BOM_UTF16_BE,
    constants.UTF_16_LE: codecs.BOM_UTF16_LE,
    constants.UTF_8_SIG: codecs.BOM_UTF8,
}

UNICODE_SIGNATURE = "\ufeff"


#
# Classes
#


class DetectionFailedError(Exception):

    """Raised when a the detection of encodings failed"""


@dataclasses.dataclass(frozen=True)
class EncodingDetectionResult:

    """Encoding detection result"""

    source: bytes
    unicode: str
    detected_encoding: str


#
# Functions
#


def detect_encoding(
    source: Union[bytes, bytearray],
    *try_encodings: str,
    check_boms: bool = True,
) -> EncodingDetectionResult:
    """Try to decode source to a unicode string
    using the provided encodings,
    and return an EncodingDetectionResult.

    If check_boms is True (= default value),
    try each of the known encodings which use a Byte Order Mark,
    defined in the global BOM_ASSIGNMENTS list.
    If one matches, decode and strip the unicode signature.
    If none of these Byte Order Marks was found, try to decode
    the source using the provided encodings in the given order.
    Return an EncodingDetectionResult on first success,
    or raise a DetectionFailedError.
    """
    source_bytes = bytes(source)
    checked_encodings: List[str] = []
    if check_boms:
        for candidate_encoding, bom in BOMS_BY_ENCODING.items():
            checked_encodings.append(candidate_encoding)
            if source_bytes.startswith(bom):
                return EncodingDetectionResult(
                    source=source_bytes,
                    unicode=source_bytes.decode(
                        candidate_encoding,
                        errors="strict",
                    ).lstrip(UNICODE_SIGNATURE),
                    detected_encoding=candidate_encoding,
                )
            #
        #
    #
    for candidate_encoding in try_encodings:
        checked_encodings.append(candidate_encoding)
        try:
            unicode = source_bytes.decode(candidate_encoding, errors="strict")
        except UnicodeDecodeError:
            continue
        #
        return EncodingDetectionResult(
            source=source_bytes,
            unicode=unicode,
            detected_encoding=candidate_encoding,
        )
    #
    raise DetectionFailedError(checked_encodings)


def to_unicode(
    source: Union[bytearray, bytes],
    *try_additional_encodings: str,
    fallback_encoding: str = DEFAULT_FALLBACK_ENCODING,
) -> str:
    """Wrap analyze.detect_encoding()
    trying ASCII, UTF-8 and the fallback encoding.
    Return the conversion result only."""
    if not isinstance(source, (bytearray, bytes)):
        raise TypeError(
            "This function requires binary input,"
            f" not {source.__class__.__name__}."
        )
    #
    return detect_encoding(
        source,
        *try_additional_encodings,
        constants.ASCII,
        constants.UTF_8,
        fallback_encoding,
    ).unicode


def anything_to_unicode(
    input_object: Any,
    *try_additional_encodings: str,
    fallback_encoding: str = DEFAULT_FALLBACK_ENCODING,
) -> str:
    """Safe wrapper around to_unicode() returning the string conversion
    of the input object if it was not a byte string
    """
    try:
        return to_unicode(
            input_object,
            *try_additional_encodings,
            fallback_encoding=fallback_encoding,
        )
    except TypeError:
        return str(input_object)
    #


def to_bytes(
    unicode_text: str,
    to_encoding: str = DEFAULT_TARGET_ENCODING,
    add_bom: bool = True,
) -> bytes:
    """Encode unicode_text to a bytes representation
    using the provided encoding
    """
    if isinstance(unicode_text, str):
        byte_string = unicode_text.encode(to_encoding)
        try:
            bom = BOMS_BY_ENCODING[to_encoding]
        except KeyError:
            return byte_string
        #
        if (
            add_bom
            and to_encoding != constants.UTF_8_SIG
            and not unicode_text.startswith(UNICODE_SIGNATURE)
        ):
            return bom + byte_string
        #
        return byte_string
    #
    raise TypeError(
        "This function requires a unicode string as input,"
        f" not {unicode_text.__class__.__name__}."
    )


def anything_to_bytes(
    input_object: Any,
    *try_additional_encodings: str,
    fallback_encoding: str = DEFAULT_FALLBACK_ENCODING,
    to_encoding: str = DEFAULT_TARGET_ENCODING,
    add_bom: bool = True,
) -> bytes:
    """Encode any given object to a bytes representation
    using the provided encoding, after decoding it to unicode
    using this modules's anything_to_unicode() function
    """
    if isinstance(input_object, str):
        unicode: str = input_object
    else:
        if to_encoding not in try_additional_encodings:
            try_additional_encodings = (to_encoding, *try_additional_encodings)
        #
        unicode = anything_to_unicode(
            input_object,
            *try_additional_encodings,
            fallback_encoding=fallback_encoding,
        )
    #
    return to_bytes(
        unicode,
        to_encoding=to_encoding,
        add_bom=add_bom,
    )


def to_utf8(unicode_text: str) -> bytes:
    """Encode unicode_text to UTF-8
    using this modules's to_bytes() function
    """
    return to_bytes(unicode_text, to_encoding=constants.UTF_8)


def anything_to_utf8(
    input_object,
    *try_additional_encodings: str,
    fallback_encoding=DEFAULT_FALLBACK_ENCODING,
) -> bytes:
    """Encode any given object to its UTF-8 representation
    using this modules's anything_to_bytes() function
    """
    return anything_to_bytes(
        input_object,
        *try_additional_encodings,
        fallback_encoding=fallback_encoding,
        to_encoding=constants.UTF_8,
    )


def fix_double_utf8_transformation(unicode: str, wrong_encoding: str) -> str:
    """Fix duplicate UTF-8 transformation,
    which is a frequent result of reading UTF-8 encoded text as 8-bit-encoded
    (using a legacy encoding like CP-125x, ISO-8859-x, KOI8-x or similar),
    resulting in characters like Ã¤Ã¶Ã¼.
    This function reverts the effect.
    """
    if wrong_encoding == constants.UTF_8:
        raise ValueError("This cannot have any effect!")
    #
    return to_unicode(
        to_bytes(unicode, to_encoding=wrong_encoding),
    )


def read_from_file(
    input_file: Union[IO, pathlib.Path, str],
    *try_additional_encodings: str,
    fallback_encoding=DEFAULT_FALLBACK_ENCODING,
) -> str:
    """Read input file and return its contents as unicode"""
    if isinstance(input_file, io.BufferedIOBase):
        file_contents = input_file.read()
    elif isinstance(input_file, (pathlib.Path, str)):
        with open(input_file, mode="rb") as real_input_file:
            file_contents = real_input_file.read()
        #
    else:
        raise TypeError(
            "read_from_file() requires either a binary file"
            " or a file name as first argument"
        )
    #
    return to_unicode(
        file_contents,
        *try_additional_encodings,
        fallback_encoding=fallback_encoding,
    )


def transcode_file(
    file_name: Union[pathlib.Path, str],
    *try_additional_encodings: str,
    fallback_encoding: str = DEFAULT_FALLBACK_ENCODING,
    to_encoding: str = DEFAULT_TARGET_ENCODING,
    add_bom: bool = True,
) -> None:
    """Read the input file and transcode it to the specified encoding in place.
    Raise a ValueError if the detected encoding is the same as the
    target encoding.
    Preserve original line endings except when specified explicitly.
    Rename the original file to the original name with the detected
    encoding name attached.
    """
    file_path = pathlib.Path(file_name)
    read_bytes_content = file_path.read_bytes()
    detection_result = detect_encoding(
        read_bytes_content,
        *try_additional_encodings,
        constants.ASCII,
        constants.UTF_8,
        fallback_encoding,
    )
    # Check content encoding and raise a ValueError
    # if the original contents were already encoded
    # as to_encoding
    newly_encoded_content = to_bytes(
        detection_result.unicode, to_encoding=to_encoding, add_bom=add_bom
    )
    if newly_encoded_content == read_bytes_content:
        raise ValueError(
            f"File {file_name!r} is already encoded"
            f" in {detection_result.detected_encoding!r}!"
        )
    #
    # rename the original file to the backup file name
    directory = file_path.parent
    stem = file_path.stem
    suffix = file_path.suffix
    backup_file_path = (
        directory / f"{stem}.{detection_result.detected_encoding}{suffix}"
    )
    shutil.move(file_path, backup_file_path)
    # Write contents to the file
    file_path.write_bytes(newly_encoded_content)


# vim:fileencoding=utf-8 autoindent ts=4 sw=4 sts=4 expandtab:
