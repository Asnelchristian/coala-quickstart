from pyprint.ConsolePrinter import ConsolePrinter
from coalib.output.printers.LogPrinter import LogPrinter
from coala_quickstart.interaction.Logo import print_welcome_message
from coala_quickstart.generation.Project import (
    get_project_dir, get_used_languages, print_used_languages)
from coala_quickstart.generation.FileGlobs import get_project_files
from coala_quickstart.generation.Bears import (
    get_bears, filter_relevant_bears, print_relevant_bears, give_bear_help)
from coala_quickstart.generation.Settings import (
    generate_settings, write_coafile)


def main():
    printer = ConsolePrinter()
    log_printer = LogPrinter(printer)

    print_welcome_message(printer)

    project_dir = get_project_dir(printer)
    project_files = get_project_files(log_printer, printer, project_dir)

    used_languages = list(get_used_languages(project_files))
    print_used_languages(printer, used_languages)

    all_bears = get_bears()
    relevant_bears = filter_relevant_bears(all_bears, used_languages)
    print_relevant_bears(printer, relevant_bears)
    give_bear_help(printer, all_bears)

    settings = generate_settings(project_dir, project_files, relevant_bears)
    write_coafile(printer, project_dir, settings)
