import os

from coala_quickstart.generation.Utilities import comma_split
from coala_quickstart.interaction.Question import ask_question
from coala_quickstart.Strings import glob_help
from coalib.collecting.Collectors import collect_files


def ask_glob_list(printer, prompt, default="**"):
    """
    Ask the user for a list of glob expressions to collect files from.

    :param printer:
        A ``ConsolePrinter`` object.
    :param prompt:
        Question to ask the user.
    :param default:
        Default value; ``**`` will match every file.
    :return:
        The list of glob expressions.
    """
    response = ask_question(
        printer,
        prompt,
        default=default)

    return comma_split(response)


def get_project_files(log_printer, printer, project_dir):
    """
    Gets the list of files matching files in the user's project directory
    after prompting for glob expressions.

    :param log_printer:
        A ``LogPrinter`` object.
    :param printer:
        A ``ConsolePrinter`` object.
    :return:
        A list of file paths matching the files.
    """
    printer.print(glob_help)
    file_globs = ask_glob_list(
        printer,
        "Which files do you want coala to run on?")
    ignore_globs = ask_glob_list(
        printer,
        "Which files do you want coala to ignore?",
        default="")
    printer.print()

    file_path_globs = [os.path.join(
        project_dir, glob_exp) for glob_exp in file_globs]
    ignore_path_globs = [os.path.join(
        project_dir, glob_exp) for glob_exp in ignore_globs]

    file_paths = collect_files(
        file_path_globs,
        log_printer,
        ignored_file_paths=ignore_path_globs)

    return file_paths
