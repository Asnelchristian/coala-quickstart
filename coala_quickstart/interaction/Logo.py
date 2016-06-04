from coala_quickstart.Strings import coala_bear_logo, welcome_messages


def text_wrap(*args, delimiter=' ', limit=80):
    """
    Breaks it wordwise when going further than ``limit`` chars. Example usage:

    >>> results = text_wrap(
    ...     "This is a line that is bigger than the limit",
    ...     limit=15)

    This would return a generator:

    >>> results
    <generator object text_wrap at 0x...>

    We can get the text per line when we iterate over it:

    >>> [x for x in results]
    ['This is a line', 'that is bigger', 'than the limit']

    :param args:
        The stuff you want to have printed.
    :param delimiter:
        Will be placed between all the args.
    :param limit:
        Char limit.
    :return:
        A list of strings, each element to be written on its own line.
    """
    output = delimiter.join(args)
    lines = output.splitlines(keepends=True)
    for line in lines:
        curr_print = line
        while len(curr_print.rstrip('\n')) > limit:
            splitpos = curr_print[:limit].rfind(' ')
            if splitpos < 0:
                # Word too long, search for a space left from limit at least
                splitpos = curr_print.find(' ')
                if splitpos < 0:
                    break  # Break out and add the long thing in the next line

            yield curr_print[:splitpos]
            curr_print = curr_print[splitpos+1:]

        yield curr_print


def print_side_by_side(printer, left=[], right=[], limit=80):
    """
    Prints the the given lines side by side. Example usage:

    >>> from pyprint.ConsolePrinter import ConsolePrinter
    >>> printer = ConsolePrinter()
    >>> print_side_by_side(
    ...     printer,
    ...     ["Text content on the left",
    ...      "side of the text."],
    ...     ["Right side should contain",
    ...      "this."],
    ...     limit=80)
    Text content on the left Right side should contain
    side of the text.        this.

    If either side is longer than the other, empty lines will
    be added to the shorter side.

    :param printer:
        A ``ConsolePrinter`` object used for console interaction.
    :param left:
        The lines for the left portion of the text.
    :param right:
        The lines for the right portion of the text.
    :param limit:
        The maximum line length limit.
    """
    max_length = limit - len(max(left, key=len))

    for line in range(len(left) - len(right)):
        right.append("")
    for line in range(len(right) - len(left)):
        left.append("")

    for left_line, right_line in zip(left, right):
        printer.print(left_line, color="white", end="")
        printer.print(" " * (limit + 1 - max_length - len(left_line)), end="")
        printer.print(right_line, color="blue")


def print_welcome_message(printer):
    """
    Prints the coala bear logo with a welcome message side by side.

    :param printer:
        A ``ConsolePrinter`` object used for console interaction.
    """
    max_length = 80 - len(max(coala_bear_logo, key=len))
    text_lines = [""]
    for welcome_message in welcome_messages:
        text_lines += [""]
        text_lines += text_wrap(welcome_message, limit=max_length)

    print_side_by_side(
        printer,
        left=coala_bear_logo,
        right=text_lines,
        limit=80)
