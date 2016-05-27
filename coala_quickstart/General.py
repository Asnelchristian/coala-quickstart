import os


from coala_quickstart.messages import (
    print_welcome_message, ask_question)
from coala_quickstart.GeneralUtilities import comma_split
from coalib.settings.ConfigurationGathering import load_configuration
from coalib.misc.DictUtilities import inverse_dicts
from coalib.collecting.Collectors import (
    collect_all_bears_from_sections, filter_section_bears_by_languages)


def get_sections(printer):
    """
    Gets the list of sections for the coafile.

    >>> from coalib.misc.ContextManagers import simulate_console_inputs
    >>> from coalib.misc.ContextManagers import suppress_stdout
    >>> from pyprint.NullPrinter import NullPrinter
    >>> printer = NullPrinter()
    >>> with simulate_console_inputs("cpp, python"), suppress_stdout():
    ...     dir = get_sections(printer)
    >>> assert dir == ["cpp", "python"]
    """
    sections_help = ("Every coafile consists one or more sections "
                     "(names are case insensitive). You may use sections to "
                     "categorize in anyway you like:"
                     "- different sections for components in different "
                     "languages\n "
                     "- different logical components\n"
                     "- different settings for components\n\n"
                     "There is a special section called the `Default` "
                     "section. All settings under the default section are "
                     "applicable to every other section. Thus this section "
                     "is used for rules you want common to all sections.")

    response = ask_question(
        printer,
        "What are the different section names for your project?",
        help_text=sections_help)

    return comma_split(response)


def get_project_dir(printer):
    """
    Retrieves the project directory from the user:

    >>> from coalib.misc.ContextManagers import simulate_console_inputs
    >>> from coalib.misc.ContextManagers import suppress_stdout
    >>> from pyprint.NullPrinter import NullPrinter
    >>> printer = NullPrinter()
    >>> with simulate_console_inputs("/abs/path"), suppress_stdout():
    ...     dir = get_project_dir(printer)
    >>> assert dir == "/abs/path"

    If he doesn't feel like giving a directory, we'll assume the current
    directory:

    >>> with simulate_console_inputs(""), suppress_stdout():
    ...     dir = get_project_dir(printer)
    >>> assert dir == abspath(".")
    """
    result = ""

    while not os.path.isdir(result):
        dir = ask_question(
            printer,
            "What is your project directory?",
            caption=os.getcwd())
        result = os.path.abspath(os.path.expanduser(dir))
        if not os.path.isdir(result):
            printer.print(
                "That is not a valid directory. Try again.",
                color="red")

    return result


def get_file_globs(printer, msg, help_text=False):
    """
    Get a list of glob expressions to collect files from.

    >>> from coalib.misc.ContextManagers import simulate_console_inputs
    >>> from coalib.misc.ContextManagers import suppress_stdout
    >>> from pyprint.NullPrinter import NullPrinter
    >>> printer = NullPrinter()
    >>> with simulate_console_inputs("**/*.py, *.c, *.h"), suppress_stdout():
    ...     file_globs = get_file_globs(printer)
    >>> assert dir == ["**/*.py", "*.c", "*.h"]
    """
    url = "http://coala.readthedocs.io/en/latest/Users/Glob_Patterns.html"
    glob_help = ("File globs are a very concise way to specify a large "
                 "number of files. You may give multiple file globs "
                 "separated by commas. To learn more about glob patterns "
                 "please visit: " + url + "\n\n"
                 "For example, you may want to include your src/ folder and "
                 "all its contents but exclude your .git directory and all "
                 ".o files. To do this, simply give `src/` for the first "
                 "question and `.git/**,**/*.o` for the second question.")

    if not help_text:
        glob_help = None
    response = ask_question(
        printer,
        msg,
        caption="comma separated globs expressions, empty to match nothing",
        help_text=glob_help)

    return comma_split(response)


def get_bears(log_printer):
    sections, _ = load_configuration(None, log_printer)
    local_bears, global_bears = collect_all_bears_from_sections(
        sections, log_printer)
    return inverse_dicts(local_bears, global_bears)


def give_bear_help(printer, results, bears):
    """
    Give the help text for each bear.
    """
    print("A coala bear is a plugin that contains the actual algorithm. "
          "It have its own native code or use an external linter. It "
          "may be language specific or language independent. This "
          "makes coala completely modularized and extensible. "
          "Currently there are 78 bears for 36 different languages.")

    if len(results) > 0:
        used_languages = [lang.lower() for lang, percent in results]

        filtered_bears = []
        bear_name_dict = {}
        for bear in bears:
            bear_name_dict[bear.name.lower()] = bear
            if isinstance(bear.LANGUAGES, tuple):
                languages = [str(lang.lower()) for lang in bear.LANGUAGES]
            else:
                languages = [bear.LANGUAGES.lower()]
            for used_language in used_languages:
                if used_language in languages or "all" in languages:
                    filtered_bears.append(bear)
                    break

        print("\nBased on the languages used in project the following "
              "bears have been identified to be relevant:")
        for bear in filtered_bears:
            printer.print("\t" + bear.name, color="cyan")

        response = ""
        while response.lower() != "none":
            response = ask_question(
                printer,
                "\nWhich bear would you like to know more about?",
                caption="enter none to move on")
            if response.lower() == "none":
                break
            if response.lower() not in bear_name_dict:
                print("There isn't a bear named '" + response + "'")
            else:
                response = response.lower()
                printer.print(bear_name_dict[response].name, color="cyan")
                desc = bear_name_dict[response].get_metadata().desc
                print(" ".join(desc.split("\n")))


def get_section_bears(printer, show_bear_pretext, bears):
    url = "https://github.com/coala-analyzer/coala-bears/wiki/Available-bears"
    if show_bear_pretext:
        give_info(
            printer,
            "You may get a list of all available bears at:\n" + url)

    while True:
        response = ask_question(
            printer,
            "Which bears do you want to include in this section?",
            caption="comma separated bear names, empty for no bears")
        selected_bears = comma_split(response)

        bear_names = [bear.name.lower() for bear in bears]
        invalid_bears = []
        for selected_bear in selected_bears:
            if selected_bear.lower() not in bear_names:
                invalid_bears.append(selected_bear)

        if len(invalid_bears) == 0:
            break
        else:
            printer.print("Invalid bears: " + ", ".join(invalid_bears))

    return response
