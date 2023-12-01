"""
This file contains methods that are related to python's defaultdict object
from the collections package.
"""

from collections import defaultdict
from typing import Callable, Type, Union

import numpy as np


def nested_ddict(depth: int, endtype: Type) -> defaultdict:
    """
    Creates defaultdict that is arbitrarily nested. For example,
    if we write `d = nested_ddict(3, list)` then we can do something
    like `d['0']['1']['2']['3'].append('stuff')`.

    Parameters:
    depth - How deep the defaultdict is
    endtype - What type the value of the deepest default dict is.
    """
    if depth == 0:
        return defaultdict(endtype)
    return defaultdict(lambda: nested_ddict(depth - 1, endtype))


def format_ddict(
    ddict: defaultdict, make_nparr: bool = True, sort_lists: bool = False
) -> defaultdict:
    """
    Turn nested defaultdicts into nested dicts and,optionally lists in numpy arrays.

    Parameters:
    ddict - Defaultdict to transform
    make_nparr - If True, will turn lists into numpy arrays
    sort_list - If True, will sort any lists it finds
    """
    # sike, `ddict` can actually be a dict, list or other object
    # but those cases are ONLY during recusive calls
    if isinstance(ddict, (dict, defaultdict)):
        ddict = {k: format_ddict(v, make_nparr, sort_lists) for k, v in ddict.items()}
    elif isinstance(ddict, list):
        ddict = sorted(ddict) if sort_lists else ddict
        ddict = np.array(ddict) if make_nparr else ddict
    return ddict


def pprint_nested_dict(
    d: dict,
    tab: int = 2,
    k_format: Union[str, Callable[..., str]] = "",
    v_format: Union[str, Callable[..., str]] = "",
    sort: bool = True,
    indentation: int = 0,
) -> None:
    """
    Prints out a nested dictionary, giving a new line and indentation.

    Parameters:
    d - Dictionary to print out
    tab (default 2) - Tab width, i.e. how many spaces per depth into the dictionary
    k_format (default "") - How to format the final key. Can be given as a string
        representing its formatting or as a callable that takes the a key as its sole
        argument.
    v_format (default "") - How to format the value of this final key. Can be given as
        a string represesnting its formatting or as a callable that takes a value as its
        sole argument.
    sort (default True) - If True, will sort the final key
    indentation (default 0) - The initial indentation
    """
    if isinstance(list(d.values())[0], dict):
        # If there's still more nesting, then run recursively
        for k, v in d.items():
            print(f"{' ' * indentation}{k}:")

            pprint_nested_dict(
                d=v,
                tab=tab,
                k_format=k_format,
                v_format=v_format,
                sort=sort,
                indentation=indentation + tab,
            )
    else:
        # Otherwise, we've reached the end, so print it out
        keys = sorted(d.keys()) if sort else d.keys()

        # Either format with method, with f-string or not at all
        for k in keys:
            if callable(k_format):
                k_str = k_format(k)
            elif k_format:
                k_str = k_format.format(k)
            else:
                k_str = k

            if callable(v_format):
                v_str = v_format(d[k])
            elif v_format:
                v_str = v_format.format(d[k])
            else:
                v_str = d[k]
            print(f"{' ' * indentation}{k_str}: {v_str}")
