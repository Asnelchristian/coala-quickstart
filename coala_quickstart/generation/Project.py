import os
import operator

from coala_utils.Question import ask_question
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
            "What is your project directory?",
            default=os.getcwd(),
            prefill=True)
        project_dir = os.path.abspath(os.path.expanduser(project_dir))
        if not os.path.isdir(project_dir):
            printer.print("Please enter a valid directory", color="blue")

    return project_dir


def get_used_languages(file_paths):
    """
    Identifies the most used languages in the user's project directory
    from the files matched from the given glob expression.

    :param file_paths:
        A list of absolute file paths in the user's project directory.
    :return:
        A list of tuples containing a language name as the first value
        and percentage usage in the project as the second value.
    """
    results = {lang: 0 for ext in exts for lang in exts[ext]}
    results["Unknown"] = 0

    for file_path in file_paths:
        ext = os.path.splitext(file_path)[1]
        if ext in exts:
            for lang in exts[ext]:
                results[lang] += 1
        else:
            results["Unknown"] += 1

    if file_paths:
        for language in results:
            results[language] = (100 * results[language]) / len(file_paths)

    languages = sorted(
        results.items(),
        key=operator.itemgetter(1),
        reverse=True)
    append_list = []
    unknown_percent = 0
    for lang, percent in languages:  # pragma: no branch
        if percent > 0:
            if lang == "Unknown":
                unknown_percent = percent
            else:
                yield (lang, percent)

    if unknown_percent > 0:
        yield ("Unknown", unknown_percent)


def print_used_languages(printer, results):
    """
    Prints the sorted list of used languages along with each language's
    percentage use.

    :param printer:
        A ``ConsolePrinter`` object used for console interactions.
    :param results:
        A list of tuples containing a language name as the first value
        and percentage usage in the project as the second value.
    """
    if results:
        printer.print(
            "The following languages have been automatically detected:")
        for lang, percent in results:
            formatted_line = "{:>25}: {:>2}%".format(lang, int(percent))
            printer.print(formatted_line, color="cyan")
        printer.print()
