# -*- coding: utf-8 -*-

"""

tests.test_transcode

Unit test the transcode module


Copyright (C) 2023 Rainer Schwarzbach

This file is part of qrstu.

qrstu is free software: you can redistribute it and/or modify
it under the terms of the MIT License.

qrstu is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the LICENSE file for more details.

"""


import pathlib
import tempfile

from unittest import TestCase

from qrstu import transcode

from . import commons


READ_BINARY = "rb"
READ_TEXT = "rt"


class Functions(TestCase):

    """Test the module functions"""

    maxDiff = None

    def test_detect_encoding(self) -> None:
        """detect_encoding() function"""
        for unicode, encoded in commons.DETERMINISTIC_DATA.items():
            for encoding, byte_string in encoded.items():
                with self.subTest(
                    encoding=encoding,
                    unicode=unicode,
                    target="success",
                ):
                    self.assertEqual(
                        transcode.detect_encoding(byte_string, encoding),
                        transcode.EncodingDetectionResult(
                            source=byte_string,
                            unicode=unicode,
                            detected_encoding=encoding,
                        ),
                    )
                #
                if encoding != commons.UTF_8:
                    with self.subTest(
                        encoding=encoding,
                        unicode=unicode,
                        target="error",
                    ):
                        self.assertRaises(
                            transcode.DetectionFailedError,
                            transcode.detect_encoding,
                            byte_string,
                            commons.UTF_8,
                        )
                    #
                #
            #
            for encoding, bom in transcode.BOMS_BY_ENCODING.items():
                byte_string = unicode.encode(encoding)
                if encoding != commons.UTF_8_SIG:
                    byte_string = bom + byte_string
                #
                with self.subTest(
                    encoding=encoding,
                    unicode=unicode,
                    target="autodetect_by_bom",
                ):
                    self.assertEqual(
                        transcode.detect_encoding(byte_string),
                        transcode.EncodingDetectionResult(
                            source=byte_string,
                            unicode=unicode,
                            detected_encoding=encoding,
                        ),
                    )
                #
            #
        #

    def test_to_unicode(self) -> None:
        """to_unicode() function"""
        for unicode, encoded in commons.DETERMINISTIC_DATA.items():
            for encoding, byte_string in encoded.items():
                with self.subTest(
                    encoding=encoding,
                    unicode=unicode,
                    target="success",
                ):
                    self.assertEqual(
                        transcode.to_unicode(byte_string, encoding),
                        unicode,
                    )
                #
            #
            with self.subTest(
                unicode=unicode,
                target="error",
            ):
                self.assertRaisesRegex(
                    TypeError,
                    "^This function requires binary input",
                    transcode.to_unicode,
                    unicode,
                )
            #
        #

    def test_anything_to_unicode(self) -> None:
        """anything_to_unicode() function"""
        for unicode, encoded in commons.DETERMINISTIC_DATA.items():
            for encoding, byte_string in encoded.items():
                with self.subTest(
                    encoding=encoding,
                    unicode=unicode,
                    source="binary",
                ):
                    self.assertEqual(
                        transcode.anything_to_unicode(byte_string, encoding),
                        unicode,
                    )
                #
            #
            with self.subTest(
                unicode=unicode,
                source="text",
            ):
                self.assertEqual(
                    transcode.anything_to_unicode(unicode),
                    unicode,
                )
            #
        #

    def test_to_bytes(self) -> None:
        """to_bytes() function"""
        for unicode, encoded in commons.DETERMINISTIC_DATA.items():
            for encoding, byte_string in encoded.items():
                with self.subTest(
                    encoding=encoding,
                    byte_string=byte_string,
                    target="success",
                ):
                    self.assertEqual(
                        transcode.to_bytes(unicode, to_encoding=encoding),
                        byte_string,
                    )
                #
                with self.subTest(
                    byte_string=byte_string,
                    target="error",
                ):
                    self.assertRaisesRegex(
                        TypeError,
                        "^This function requires a unicode string as input",
                        transcode.to_bytes,
                        byte_string,
                    )
                #
            #
            for encoding, bom in transcode.BOMS_BY_ENCODING.items():
                byte_string = unicode.encode(encoding)
                byte_string_with_bom = byte_string
                if encoding != commons.UTF_8_SIG:
                    byte_string_with_bom = bom + byte_string
                #
                with self.subTest(
                    encoding=encoding,
                    unicode=unicode,
                    target="with bom",
                ):
                    self.assertEqual(
                        transcode.to_bytes(
                            unicode, to_encoding=encoding, add_bom=True
                        ),
                        byte_string_with_bom,
                    )
                #
                with self.subTest(
                    encoding=encoding,
                    unicode=unicode,
                    target="without bom",
                ):
                    self.assertEqual(
                        transcode.to_bytes(
                            unicode, to_encoding=encoding, add_bom=False
                        ),
                        byte_string,
                    )
                #
            #
        #

    def test_anything_to_bytes(self) -> None:
        """anything_to_bytes() function"""
        for unicode, encoded in commons.DETERMINISTIC_DATA.items():
            for encoding, byte_string in encoded.items():
                with self.subTest(
                    encoding=encoding,
                    byte_string=byte_string,
                    source="text",
                ):
                    self.assertEqual(
                        transcode.anything_to_bytes(
                            unicode, to_encoding=encoding
                        ),
                        byte_string,
                    )
                #
                with self.subTest(
                    encoding=encoding,
                    byte_string=byte_string,
                    source="binary",
                ):
                    self.assertEqual(
                        transcode.anything_to_bytes(
                            byte_string, to_encoding=encoding
                        ),
                        byte_string,
                    )
                #
            #
        #

    def test_to_utf8(self) -> None:
        """to_utf8() function"""
        for unicode in commons.DETERMINISTIC_DATA:
            byte_string = unicode.encode(commons.UTF_8)
            with self.subTest(
                unicode=unicode,
                target="success",
            ):
                self.assertEqual(
                    transcode.to_utf8(unicode),
                    byte_string,
                )
            #
            with self.subTest(
                unicode=unicode,
                target="error",
            ):
                self.assertRaisesRegex(
                    TypeError,
                    "^This function requires a unicode string as input",
                    transcode.to_utf8,
                    byte_string,
                )
            #
        #

    def test_anything_to_utf8(self) -> None:
        """anything_to_utf8() function"""
        for unicode in commons.DETERMINISTIC_DATA:
            byte_string = unicode.encode(commons.UTF_8)
            with self.subTest(
                unicode=unicode,
                source="text",
            ):
                self.assertEqual(
                    transcode.anything_to_utf8(unicode),
                    byte_string,
                )
            #
            with self.subTest(
                unicode=unicode,
                source="binary",
            ):
                self.assertEqual(
                    transcode.anything_to_utf8(unicode),
                    byte_string,
                )
            #
        #

    def test_fix_double_utf8_transformation(self) -> None:
        """fix_double_utf8_transformation() function"""
        for encoding, examples in commons.GUESS_DATA.items():
            for text in examples:
                with self.subTest(encoding=commons.UTF_8, text=text):
                    self.assertRaisesRegex(
                        ValueError,
                        "^This cannot have any effect!",
                        transcode.fix_double_utf8_transformation,
                        text.encode(commons.UTF_8),
                        wrong_encoding=commons.UTF_8,
                    )
                #
                with self.subTest(encoding=encoding, text=text):
                    double_decoded = text.encode(commons.UTF_8).decode(
                        encoding, errors=commons.ERRORS_IGNORE
                    )
                    self.assertEqual(
                        transcode.fix_double_utf8_transformation(
                            double_decoded,
                            wrong_encoding=encoding,
                        ),
                        text,
                    )
                #
            #
        #

    def test_read_from_file(self) -> None:
        """read_from_file() function"""
        all_testdata = dict(commons.DETERMINISTIC_DATA)
        source_text, encoded = all_testdata.popitem()
        # test_file_suffix = ".txt"
        with tempfile.TemporaryDirectory() as tempdir:
            for encoding, byte_string in encoded.items():
                text_file_path = pathlib.Path(tempdir) / f"{encoding}.txt"
                text_file_path.write_bytes(byte_string)
                try_other_encodings = []
                if encoding not in (commons.ASCII, commons.UTF_8):
                    try_other_encodings.append(encoding)
                #
                with self.subTest(
                    source_text=source_text,
                    encoding=encoding,
                    scope="text file",
                ):
                    with open(
                        text_file_path, mode=READ_TEXT, encoding=encoding
                    ) as input_file:
                        self.assertRaisesRegex(
                            TypeError,
                            "^read_from_file\\(\\) requires either a"
                            " binary file or a file name as first argument",
                            transcode.read_from_file,
                            input_file,
                            *try_other_encodings,
                        )
                    #
                #
                with self.subTest(
                    source_text=source_text,
                    encoding=encoding,
                    scope="binary file",
                ):
                    with open(text_file_path, mode=READ_BINARY) as input_file:
                        self.assertEqual(
                            transcode.read_from_file(
                                input_file, *try_other_encodings
                            ),
                            source_text,
                        )
                    #
                #
                with self.subTest(
                    source_text=source_text,
                    encoding=encoding,
                    scope="path",
                ):
                    self.assertEqual(
                        transcode.read_from_file(
                            text_file_path, *try_other_encodings
                        ),
                        source_text,
                    )
                #
                with self.subTest(
                    source_text=source_text,
                    encoding=encoding,
                    scope="str",
                ):
                    self.assertEqual(
                        transcode.read_from_file(
                            str(text_file_path), *try_other_encodings
                        ),
                        source_text,
                    )
                #
            #
        #

    def test_transcode_file(self) -> None:
        """transcode_file() function"""
        all_testdata = dict(commons.DETERMINISTIC_DATA)
        source_text, encoded = all_testdata.popitem()
        all_encodings = list(encoded)
        # test_file_suffix = ".txt"
        with tempfile.TemporaryDirectory() as tempdir:
            for encoding, byte_string in encoded.items():
                try_other_encodings = []
                if encoding not in (commons.ASCII, commons.UTF_8):
                    try_other_encodings.append(encoding)
                #
                for tested_encoding in all_encodings:
                    text_file_path = pathlib.Path(tempdir) / f"{encoding}.txt"
                    text_file_path.write_bytes(byte_string)
                    if tested_encoding == encoding:
                        with self.subTest(
                            "Error: file already in the expected encoding",
                            source_text=source_text,
                            encoding=encoding,
                            tested_encoding=tested_encoding,
                        ):
                            self.assertRaisesRegex(
                                ValueError,
                                "^File ",
                                transcode.transcode_file,
                                text_file_path,
                                *try_other_encodings,
                                to_encoding=tested_encoding,
                            )
                        #
                    else:
                        transcode.transcode_file(
                            text_file_path,
                            *try_other_encodings,
                            to_encoding=tested_encoding,
                        )
                        with self.subTest(
                            "Trascoding result",
                            source_text=source_text,
                            encoding=encoding,
                            tested_encoding=tested_encoding,
                        ):
                            self.assertEqual(
                                source_text.encode(tested_encoding),
                                text_file_path.read_bytes(),
                            )
                        #
                        with self.subTest(
                            "Backup file containing original contents",
                            source_text=source_text,
                            encoding=encoding,
                            tested_encoding=tested_encoding,
                        ):
                            backup_file_path = (
                                pathlib.Path(tempdir)
                                / f"{encoding}.{encoding}.txt"
                            )
                            self.assertEqual(
                                backup_file_path.read_bytes(),
                                byte_string,
                            )
                        #
                    #
                #
            #
        #


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
