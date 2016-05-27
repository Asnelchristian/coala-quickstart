import os

from pyprint.ConsolePrinter import ConsolePrinter

from coalib.output.printers.LogPrinter import LogPrinter
from coalib.collecting.Collectors import collect_files
from coala_quickstart.messages import (
    print_welcome_message, give_info)
from coala_quickstart.General import (
    get_project_dir, get_sections, get_file_globs, get_bears,
    give_bear_help, get_section_bears)
from coala_quickstart.Utilities import get_popular_languages
from coala_quickstart.ConfWriter import write_coafile


def main():
    printer = ConsolePrinter()
    log_printer = LogPrinter(printer)

    print_welcome_message(printer)

    project_dir = get_project_dir(printer)

    file_globs = get_file_globs(
        printer,
        msg="Which files do you want to lint?",
        help_text=True)
    ignore_file_globs = get_file_globs(
        printer,
        msg="Which files do you want to ignore?",
        help_text=False)

    path_globs = []
    ignore_globs = []
    for file_glob in file_globs:
        path_globs.append(os.path.join(project_dir, file_glob))
    for ignore_file_glob in ignore_file_globs:
        ignore_globs.append(os.path.join(project_dir, ignore_file_glob))

    file_paths = collect_files(
        path_globs,
        log_printer,
        ignored_file_paths=ignore_globs)
    give_info(printer, str(len(file_paths)) + " file(s) matched!")

    results = get_popular_languages(file_paths)
    if len(results):
        print("\nThe following languages have been automatically detected:")
        for lang, percent in results:
            printer.print(
                "\t" + lang + " (" + str(percent) + "%)", color="cyan")
        print("")
    bears = get_bears(log_printer)
    give_bear_help(printer, results, bears)
    print("")

    sections = ["Default"] + get_sections(printer)
    filtered_sections = []
    for section in sections:
        if section not in filtered_sections:
            filtered_sections.append(section)

    bear_pre_text = False
    settings = {}
    for section in filtered_sections:
        printer.print("[" + section + "]", color="green")
        selected_bears = get_section_bears(printer, bear_pre_text, bears)
        settings[section] = {"bears": selected_bears}

    write_coafile(project_dir, settings)

    give_info(
        printer,
        "That's it! Go to your project directory and run `coala` "
        "for awesome automatic code analysis!")
