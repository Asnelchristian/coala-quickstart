import os
import unittest

from pyprint.ConsolePrinter import ConsolePrinter
from coalib.misc.ContextManagers import (
    simulate_console_inputs, suppress_stdout, retrieve_stdout)
from coala_quickstart.generation.Project import (
    get_project_dir, get_used_languages, print_used_languages)


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

class TestPopularLanguages(unittest.TestCase):

    def setUp(self):
        self.printer = ConsolePrinter()

    def test_get_used_languages(self):
        file_lists = [["/tmp/file.py", "/tmp/file.py"],
            ["/tmp/file.py", "/tmp/test.cpp"],
            ["/tmp/file.py"],
            ["/tmp/file.py", "/tmp/unknown.extension"],
            ["/tmp/unknown.extension"],
            []]
        results = [[('Python', 100)],
            [('Python', 50), ('C++', 50)],
            [('Python', 100)],
            [('Python', 50), ('Unknown', 50)],
            [('Unknown', 100)],
            []]

        for file_list, expected_result in zip(file_lists, results):
            result = get_used_languages(file_list)
            self.assertEqual(sorted(result), sorted(expected_result))

    def test_print_used_languages(self):
        with retrieve_stdout() as custom_stdout:
            print_used_languages(self.printer, [('Python', 100)])
            res = custom_stdout.getvalue()
            self.assertIn("Python", res)
            self.assertIn("100%", res)
            self.assertNotIn("Unknown", res)

        with retrieve_stdout() as custom_stdout:
            print_used_languages(self.printer, [('Python', 75), ('C++', 25)])
            self.assertIn("75%\n", custom_stdout.getvalue())

    def test_no_results(self):
        with retrieve_stdout() as custom_stdout:
            print_used_languages(self.printer, [])
            self.assertNotIn("following langauges", custom_stdout.getvalue())
