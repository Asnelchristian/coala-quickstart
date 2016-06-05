import sys
import os
import unittest
from copy import deepcopy

from pyprint.ConsolePrinter import ConsolePrinter
from coalib.output.printers.LogPrinter import LogPrinter
from coalib.misc.ContextManagers import (
    simulate_console_inputs, suppress_stdout, retrieve_stdout)
from coala_quickstart.generation.Bears import (
    get_bears, filter_relevant_bears, print_relevant_bears, give_bear_help)

class TestBears(unittest.TestCase):

    def setUp(self):
        self.printer = ConsolePrinter()
        self.log_printer = LogPrinter(self.printer)
        old_argv = deepcopy(sys.argv)
        del sys.argv[1:]
        self.bears = get_bears()
        sys.argv = old_argv

    def test_filter_relevant_bears(self):
        res = filter_relevant_bears(self.bears, [('Python', 70), ('YAML', 20), ('Unknown', 10)])
        self.assertIn("YAML", res)
        self.assertIn("Python", res)
        self.assertIn("All", res)
        self.assertTrue(len(res["YAML"]) > 0)
        self.assertTrue(len(res["Python"]) > 0)
        self.assertTrue(len(res["All"]) > 0)

    def test_print_relevant_bears(self):
        with retrieve_stdout() as custom_stdout:
            print_relevant_bears(self.printer, filter_relevant_bears(
                self.bears, [('Python', 70), ('Unknown', 30)]))
            self.assertIn("PEP8Bear", custom_stdout.getvalue())

    def test_give_bear_help(self):
        with retrieve_stdout() as custom_stdout, simulate_console_inputs("PEP8Bear", "none"):
            give_bear_help(self.printer, self.bears)
            self.assertIn("fixes PEP8", custom_stdout.getvalue())
            self.assertNotIn("There isn't a bear named", custom_stdout.getvalue())

    def test_invalid_bear_help(self):
        with retrieve_stdout() as custom_stdout, simulate_console_inputs("InvalidBear", "none"):
            give_bear_help(self.printer, self.bears)
            self.assertIn("There isn't a bear named", custom_stdout.getvalue())
