import os
import unittest

from pyprint.ConsolePrinter import ConsolePrinter
from coalib.misc.ContextManagers import suppress_stdout, retrieve_stdout
from coala_quickstart.generation.Project import get_project_dir


class TestQuestion(unittest.TestCase):

    def setUp(self):
        self.printer = ConsolePrinter()

# End of file
