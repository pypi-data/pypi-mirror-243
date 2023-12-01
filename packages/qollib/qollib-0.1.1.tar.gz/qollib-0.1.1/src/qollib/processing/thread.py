#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The threads hold information on the function (and result) to execute in a thread or process.

@author: hoelken
"""

import logging

from concurrent.futures import Executor

log = logging.getLogger()


class Thread:
    """
    # Thread
    The threads hold information on the function to execute in a thread or process.
    Provides an interface to the `future` object once submitted to an executer.
    """

    def __init__(self, func: callable, args: object):
        self.function = func
        self.arguments = args
        self.future = None

    def submit(self, executor: Executor):
        """Start execution via executor"""
        if not self.is_submitted():
            self.future = executor.submit(self.function, self.arguments)
        return self

    def is_submitted(self) -> bool:
        return self.future is not None

    def is_done(self) -> bool:
        return self.is_submitted() and self.future.done()

    @property
    def exception(self):
        if not self.is_done():
            return None
        return self.future.exception()

    @property
    def result(self):
        if not self.is_submitted():
            return None
        return self.future.result()

    def cancel(self):
        try:
            self.future.cancel()
        except RuntimeError as e:
            log.warning('Unable to cancel thread: %s', e)
