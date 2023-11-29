# -*- coding: utf-8 -*-

""" Module summary description.

More detailed description.
"""


def check_string(string, list_of_strings):
    """ Check validity of and return string against list of valid strings

    :param string: searched string
    :param list_of_strings: list/tuple/set of valid strings string is to be checked against
    :return: validate string from list of strings if match
    """

    output_string = []

    for item in list_of_strings:
        if item.lower().startswith(string.lower()):
            output_string.append(item)

    if len(output_string) == 1:
        return output_string[0]
    elif len(output_string) == 0:
        raise ValueError("input must match one of those: {}".format(list_of_strings))
    elif len(output_string) > 1:
        raise ValueError("input match more than one valid value among {}".format(list_of_strings))


def str_to_list(a_string):
    """ Convert string to list

    :param a_string: a string or a collection
    :return: a collection of lists or the same object
    """
    try:
        return a_string.splitlines()
    except AttributeError:
        return a_string


def lazyproperty(func):
    name = '_lazy_' + func.__name__

    @property
    def lazy(self):
        if hasattr(self, name):
            return getattr(self, name)
        else:
            value = func(self)
            setattr(self, name, value)
            return value
    return lazy
