from pyprint.NullPrinter import NullPrinter

from coalib.misc.Constants import FALSE_STRINGS
from coala_quickstart.Strings import bear_help
from coala_quickstart.interaction.Question import ask_question
from coalib.settings.ConfigurationGathering import load_configuration
from coalib.misc.DictUtilities import inverse_dicts
from coalib.collecting.Collectors import (
    collect_all_bears_from_sections, filter_section_bears_by_languages)
from coalib.output.printers.LogPrinter import LogPrinter


def get_bears():
    """
    Get a dict of bears with the bear class as key.

    :return:
        A dict with bear classes as key and the list of sections
        as value.
    """
    log_printer = LogPrinter(NullPrinter())
    sections = load_configuration(None, log_printer)[0]
    local_bears, global_bears = collect_all_bears_from_sections(
        sections, log_printer)
    return inverse_dicts(local_bears, global_bears)


def filter_relevant_bears(bears, used_langauges):
    """
    From the bear dict, filter the bears per relevant language.

    :param bears:
        A dict of bears classes as key and the list of sections
        as value.
    :param used_langauges:
        A list of tuples with language name as the first element
        and percentage usage as the second element; sorted by
        percentage usage.
    :return:
        A dict with language name as key and bear classes as value.
    """
    lang_map = {"all": "All"}
    relevant_bears = {"All": []}
    for lang in used_langauges:
        if lang[0] == "Unknown":
            continue
        lang_map[lang[0].lower()] = lang[0]
        relevant_bears[lang[0]] = []

    for bear in bears:
        bear_languages = [str(lang.lower()) for lang in bear.LANGUAGES]
        for bear_lang in bear_languages:
            if bear_lang in lang_map and lang_map[bear_lang] in relevant_bears:
                relevant_bears[lang_map[bear_lang]].append(bear)
    return relevant_bears


def print_relevant_bears(printer, relevant_bears):
    """
    Prints the relevant bears in sections separated by language.

    :param printer:
        A ``ConsolePrinter`` object used for console interactions.
    :param relevant_bears:
        A dict with language name as key and bear classes as value.
    """
    printer.print(bear_help)
    printer.print("\nBased on the languages used in project the following "
                  "bears have been identified to be relevant:")
    for language in relevant_bears:
        printer.print("\t[" + language + "]", color="green")
        for bear in relevant_bears[language]:
            printer.print("\t" + bear.name, color="cyan")
        printer.print("")


def give_bear_help(printer, all_bears):
    """
    Ask the user for a bear name and display the bear description.

    :param printer:
        A ``ConsolePrinter`` object used for console interactions.
    :param all_bears:
        A dict with bear classes as key and the list of sections
        as value.
    """
    response = ""
    bear_name_dict = {}
    for bear in all_bears:
        bear_name_dict[bear.name.lower()] = bear

    while response.lower() not in FALSE_STRINGS:  # pragma: no branch
        response = ask_question(
            printer,
            "Which bear would you like to know more about?",
            default="none")
        if response.lower() in FALSE_STRINGS:
            break
        if response.lower() not in bear_name_dict:
            printer.print("There isn't a bear named '" + response + "'.")
        else:
            response = response.lower()
            printer.print("\n" + bear_name_dict[response].name, color="cyan")
            desc = bear_name_dict[response].get_metadata().desc
            print(" ".join(desc.split("\n")) + "\n")
