# -*- coding: utf-8 -*-

"""

qrstu.guess

Functions to guess encoding accidents


Copyright (C) 2023 Rainer Schwarzbach

This file is part of qrstu.

qrstu is free software: you can redistribute it and/or modify
it under the terms of the MIT License.

qrstu is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the LICENSE file for more details.

"""


import logging

from collections import Counter
from typing import Iterator, Tuple

from qrstu import guess_data
from qrstu import transcode


def double_encoding_producer_candidates(
    source: str,
) -> Iterator[Tuple[str, int]]:
    """Determine candidate encodings that might be used to produce source,
    and return an Interator
    """
    logging.debug("Text: %r", source)
    for encoding, fragments in guess_data.SUSPICIOUS_FRAGMENTS.items():
        matches: Counter[str] = Counter()
        for single_fragment in fragments:
            if single_fragment in source:
                matches.update(
                    {single_fragment: source.count(single_fragment)}
                )
            #
        #
        if matches:
            logging.debug(
                " - Matches in %r → %s",
                encoding,
                ", ".join(
                    f"{count} × {fragment!r}"
                    for fragment, count in matches.items()
                ),
            )
            yield ((encoding, len(matches)))
        #
    #


def most_probable_producer(source: str) -> str:
    """Guess which encoding was most probably used to produce source"""
    matches = [
        (counts, encoding)
        for (encoding, counts) in double_encoding_producer_candidates(source)
    ]
    print(matches)
    if not matches:
        raise ValueError("No hints to double encoding found")
    #
    most_matches = max(counts for counts, _ in matches)
    return [
        encoding for counts, encoding in matches if counts == most_matches
    ][0]


def fix_double_transformation(source: str) -> str:
    """Guess which encoding produced source, and fix double transformation"""
    return transcode.fix_double_utf8_transformation(
        source,
        most_probable_producer(source),
    )


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
