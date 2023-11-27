# -*- coding: utf-8 -*-

"""

tests.test_guess

Unit test the guess module


Copyright (C) 2023 Rainer Schwarzbach

This file is part of qrstu.

qrstu is free software: you can redistribute it and/or modify
it under the terms of the MIT License.

qrstu is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the LICENSE file for more details.

"""


from unittest import TestCase

from qrstu import guess

from . import commons


class Functions(TestCase):

    """Test the module functions"""

    def test_most_probable_producer(self) -> None:
        """most_probable_producer() function"""
        for encoding, examples in commons.GUESS_DATA.items():
            for text in examples:
                with self.subTest(encoding=encoding, text=text):
                    double_decoded = text.encode(commons.UTF_8).decode(
                        encoding, errors=commons.ERRORS_IGNORE
                    )
                    self.assertEqual(
                        guess.most_probable_producer(double_decoded), encoding
                    )
                #
            #
        #
        with self.subTest("No double encoding"):
            self.assertRaises(
                ValueError,
                guess.most_probable_producer,
                "Text without suspicious character sequences",
            )
        #

    def test_fix_double_transformation(self) -> None:
        """fix_double_transformation() function"""
        for encoding, examples in commons.GUESS_DATA.items():
            for text in examples:
                with self.subTest(encoding=encoding, text=text):
                    double_decoded = text.encode(commons.UTF_8).decode(
                        encoding, errors=commons.ERRORS_IGNORE
                    )
                    self.assertEqual(
                        guess.fix_double_transformation(double_decoded), text
                    )
                #
            #
        #


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
