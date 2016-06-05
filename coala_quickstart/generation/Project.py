import os

from coala_quickstart.interaction.Question import ask_question
from coala_quickstart.Extensions import exts


def get_project_dir(printer):
    """
    Retrieves the project directory from the user.

    :param printer:
        A ``ConsolePrinter`` object.
    :return:
        An absolute path to the user's project directory.
    """
    project_dir = ""

    while not os.path.isdir(project_dir):
        project_dir = ask_question(
            printer,
            "What is your project directory?",
            default=os.getcwd())
        project_dir = os.path.abspath(os.path.expanduser(project_dir))
        if not os.path.isdir(project_dir):
            printer.print("Please enter a valid directory", color="blue")

    return project_dir
