import sys


def print_welcome_message(printer):
    coala_bear_logo = [" .o88Oo._",
                       "d8P         .ooOO8bo._",
                       "88                  '*Y8bo.",
                       "YA                      '*Y8b   __",
                       " YA                        68o68**8Oo.",
                       "  \"8D                       *\"'    \"Y8o",
                       "   Y8     'YB                       .8D",
                       "   '8               d8'             8D",
                       "    8       d8888b          d      AY",
                       "    Y,     d888888         d'  _.oP\"",
                       "     q.    Y8888P'        d8",
                       "      \"q.  `Y88P'       d8\"",
                       "         Y           ,o8P",
                       "              oooo888P\"",
                       ""]
    welcome_messages = ["Hi there! Awesome you decided to do some high "
                        "quality coding. coala is just the tool you need!",
                        "You can configure coala to meet your needs. This "
                        "is done with a settings file called a `.coafile` "
                        "in the project directory.",
                        "We can help you with that. Let's get started with "
                        "some basic questions."]
    start_line = 3

    current_line = 1
    max_length = 0
    word_index = 0
    paragraphs = []
    current_para = 0

    for line in coala_bear_logo:
        max_length = max(max_length, len(line))
    for welcome_message in welcome_messages:
        paragraphs.append(welcome_message.split(" "))
        paragraphs.append([""])

    sys.stdout.write("\n")
    for line in coala_bear_logo:
        printer.print(" " + line, color="white", end="")

        if current_line >= start_line and current_para < len(paragraphs):
            words = paragraphs[current_para]
            if word_index < len(words):
                padding = max_length - len(line) + 2
                allowed_length = 79
                printed_length = max_length + 2
                printer.print(" " * padding, color="white", end="")

                while (printed_length < allowed_length and
                       word_index < len(words)):
                    left_length = allowed_length - printed_length
                    if len(words[word_index]) < left_length:
                        printer.print(words[word_index] +
                                      " ", color="blue", end="")
                        printed_length += len(words[word_index]) + 1
                        word_index += 1
                    else:
                        break

                if word_index == len(words):
                    word_index = 0
                    current_para += 1

        printer.print("", color="blue")
        current_line += 1


def ask_question(printer, question, caption=None, help_text=None):
    if help_text:
        printer.print(help_text)
    printer.print(question, color="yellow", end=" ")
    if caption:
        printer.print("(" + caption + ")", end=" ")
    print("")
    answer = input()
    print("")
    return answer


def give_info(printer, info):
    printer.print(info, color="blue")
