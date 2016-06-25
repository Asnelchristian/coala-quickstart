from coala_quickstart.generation.Utilities import comma_split
from coala_quickstart.interaction.Question import ask_question


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
