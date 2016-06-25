import os
import unittest

from pyprint.ConsolePrinter import ConsolePrinter
from coalib.output.printers.LogPrinter import LogPrinter
from coalib.misc.ContextManagers import (
    simulate_console_inputs, suppress_stdout, retrieve_stdout)
from coala_quickstart.generation.FileGlobs import ask_glob_list

class TestQuestion(unittest.TestCase):

    def setUp(self):
        self.printer = ConsolePrinter()
        self.log_printer = LogPrinter(self.printer)

    def test_ask_glob_list(self):
        with retrieve_stdout() as custom_stdout, simulate_console_inputs(""):
            response = ask_glob_list(self.printer, "Question")
            self.assertEqual(response, ["**"])

        with retrieve_stdout() as custom_stdout, simulate_console_inputs("src/**, docs/**"):
            response = ask_glob_list(self.printer, "Question")
            self.assertEqual(response, ["src/**", "docs/**"])

        with retrieve_stdout() as custom_stdout, simulate_console_inputs(""):
            response = ask_glob_list(self.printer, "Question", default="*.cpp,*.c")
            self.assertEqual(response, ["*.cpp", "*.c"])
