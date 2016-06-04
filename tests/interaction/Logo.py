import unittest

from pyprint.ConsolePrinter import ConsolePrinter
from coalib.misc.ContextManagers import (
    simulate_console_inputs, suppress_stdout, retrieve_stdout)
from coala_quickstart.interaction.Logo import (
    print_welcome_message, text_wrap, print_side_by_side)


class TestLogo(unittest.TestCase):

    def setUp(self):
        self.printer = ConsolePrinter()

    def test_text_wrap(self):
        res = [x for x in text_wrap(
            "a long sentence longer than the limit", limit=30)]
        self.assertEqual(len(res), 2)

        res = [x for x in text_wrap(
            "areallylongwordthatisgreaterthanthelimit", limit=30)]
        self.assertEqual(len(res), 1)

        res = [x for x in text_wrap("quite small words that fit", limit=30)]
        self.assertEqual(len(res), 1)

        res = [x for x in text_wrap(
            "areallylongwordfollowedby a smaller word", limit=20)]
        self.assertEqual(len(res), 2)

    def test_print_side_by_side(self):
        with retrieve_stdout() as custom_stdout:
            print_side_by_side(
                self.printer,
                ["Left side content."],
                ["Right side content",
                 "that is longer than the",
                 "left side."],
                limit=80)
            self.assertIn(
                "side content.\x1b[0m \x1b[34mRight side", custom_stdout.getvalue())

    def test_print_welcome_message(self):
        with retrieve_stdout() as custom_stdout:
            print_welcome_message(self.printer)
            self.assertIn("o88Oo", custom_stdout.getvalue())
