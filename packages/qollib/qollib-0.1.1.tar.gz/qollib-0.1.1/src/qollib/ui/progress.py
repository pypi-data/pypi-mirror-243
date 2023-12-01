#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
module provides functions to print progress to the shell (and only the shell)
"""

RESET = '\033[1;0m'
GREEN = '\033[1;32m'
RED = '\033[1;31m'


def dot(success: bool = True, flush: bool = False, char: str = '*') -> None:
    """Print a progress dot to std. out"""
    if flush:
        print('')
    else:
        print(f'{GREEN if success else RED}{char}{RESET}', end='', flush=True)


def msg(txt: str = '', flush: bool = False) -> None:
    if flush:
        print('')
    else:
        print(txt, end='\r', flush=True)


def bar(current: float, total: float, flush: bool = False, length: int = 50) -> None:
    """print a progress bar and a percent of completion to std. out """
    percent = (current * 100) / total
    done = int(round(length * (percent/100)))
    prog = ''.join(['━' for _ in range(done)])
    empty = ''.join([' ' for _ in range(length - done)])
    stop = '┃' if len(empty) > 0 else '┫'
    print(f'┣{prog}{empty}{stop} \t[{percent:.2f} %]', end='\r', flush=True)
    if flush:
        print('')
