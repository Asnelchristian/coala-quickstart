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


def generate_glob_exps(project_files, extensions, project_dir):
    """
    Generate glob expressions that matches exactly the files
    with the given extensions in the user's project directory.

    :param project_files:
        The list of files to match.
    :param extensions:
        A list of file extensions.
    :param project_dir:
        The user's project directory.
    :return:
        A tuple with the first element (a list of glob expressions)
        representing files to include and the second element (a list
        of glob expressions) representing the files to exclude.
    """
    included_globs = []
    excluded_globs = []

    for root, dirs, files in os.walk(project_dir):
        included_files = {}
        excluded_files = {}
        for file in files:
            name, ext = os.path.splitext(file)
            if ext not in extensions:
                continue

            file = os.path.join(root, file)
            if file in project_files:
                included_files.setdefault(ext, []).append(file)
            else:
                excluded_files.setdefault(ext, []).append(file)

        for extension in included_files:
            if extension not in excluded_files:
                included_globs.append(os.path.join(root, "*" + extension))
            else:
                if (len(included_files[extension]) >=
                        len(excluded_files[extension])):
                    included_globs.append(os.path.join(root, "*" + extension))
                    for excluded_file in excluded_files[extension]:
                        excluded_globs.append(excluded_file)
                    del excluded_files[extension]
                else:
                    for included_file in included_files[extension]:
                        included_globs.append(included_file)
                    del excluded_files[extension]

        for extension in excluded_files:
            excluded_globs.append(os.path.join(root, "*" + extension))

    included_globs = [os.path.relpath(
        included_glob, project_dir) for included_glob in included_globs]
    excluded_globs = [os.path.relpath(
        excluded_glob, project_dir) for excluded_glob in excluded_globs]

    return included_globs, excluded_globs
