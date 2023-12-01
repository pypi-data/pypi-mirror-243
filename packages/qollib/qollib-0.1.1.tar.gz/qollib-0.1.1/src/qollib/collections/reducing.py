#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The `reducing` utilities provides methods to reduce (dimensions) of arrays.

@author: hoelken
"""
from typing import Iterable


def flatten_sorted(lists: Iterable) -> list:
    """Flattens a list of lists and sorts the result"""
    result = flatten(lists)
    result.sort()
    return result


def flatten(lists: Iterable) -> list:
    """Flattens a list of lists and sorts the result"""
    result = []
    for entry in lists:
        if isinstance(entry, Iterable) and not isinstance(entry, (str, dict)):
            result.extend(flatten(entry))
        else:
            result.append(entry)
    return result
