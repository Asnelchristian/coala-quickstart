def ask_question(printer, question, default=None):
    """
    Asks the user a question and returns the answer.

    :param printer:
        A ``ConsolePrinter`` object used for console interactions.
    :param question:
        The question text.
    :param default:
        A default placed next to the question; used as the default
        value if the response is empty.
    """
    printer.print("")
    printer.print(question, color="yellow", end=" ")
    if default:
        printer.print("[" + default + "]", end=" ")
    printer.print("")

    answer = input()
    if default and len(answer) == 0:
        answer = default

    return answer
