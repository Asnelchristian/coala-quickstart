import os
import unittest

from pyprint.ConsolePrinter import ConsolePrinter
from coalib.misc.ContextManagers import (
    simulate_console_inputs, suppress_stdout)
from coala_quickstart.generation.Project import get_project_dir


class TestQuestion(unittest.TestCase):

    def setUp(self):
        self.printer = ConsolePrinter()

    def test_get_project_dir_absolute(self):
        with simulate_console_inputs("/tmp"), suppress_stdout():
            project_dir = get_project_dir(self.printer)
            self.assertEqual(project_dir, "/tmp")

    def test_get_project_dir_empty(self):
        with simulate_console_inputs(""), suppress_stdout():
            project_dir = get_project_dir(self.printer)
            self.assertEqual(project_dir, os.getcwd())

    def test_get_project_dir_invalid(self):
        with simulate_console_inputs("/invaliddir", "/tmp"), suppress_stdout():
            project_dir = get_project_dir(self.printer)
            self.assertEqual(project_dir, "/tmp")
