# -*- coding: utf-8 -*-

SPECIAL_SYMBOLS = set([".", "*", "?", "+", "^", "$", "|", "[", "[^", "]", "(", ")", "{", "}"])


def alphabet(re):
    """Get the associated alphabet of the given regular expression.

    :param re: Regular expression as a string.

    :return: The alphabet set.
    """
    return set(c for c in re if c not in SPECIAL_SYMBOLS)
