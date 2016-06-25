from coalib.parsing.StringProcessing import unescaped_split


def comma_split(response):
    """
    Splits the comma-separated string into a list. This takes escapes into
    consideration.

    :param response:
        Comma-separated string.
    :return:
        A list of comma-separated elements in the string.
    """
    return [x for x in unescaped_split(
        "[, ]", response, use_regex=True, remove_empty_matches=True)]
