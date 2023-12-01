#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mocks for testing multi processing functionality.

@author: hoelken
"""


def sequentially(func, args, workers=None):
    """
    Method mimics the `simultaneous` or `threaded` methods, but calls everything in sequence.
    :param func: function to call
    :param args: arguments to call the function with
    :param workers: Ignored
    :return: result of the call.
    """
    return list(func(arg) for arg in args)
