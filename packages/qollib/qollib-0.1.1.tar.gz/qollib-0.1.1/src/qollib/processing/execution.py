#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
provides housekeeping / setup methods to reduce the programming overhead of spawning threads or processes.
"""

import os
import subprocess
import time
import logging
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from functools import partial

from .thread import Thread


log = logging.getLogger()


CPU_LIM = round(os.cpu_count() * 0.7)
"""70% of CPUs from the current machine (max usage limit)"""


def threaded(func, args, workers=10, raise_exception=True):
    """
    Calls the given function in multiple threads for the set of given arguments
        Note that this does not spawn processes, but threads. Use this for non CPU
        CPU dependent tasks, i.e. I/O
    Method returns once all calls are done.

    ### Params
    - func: [Function] the function to call
    - args: [Iterable] the 'list' of arguments for each call
    - workers: [Integer] the number of concurrent threads to use
    - raise_exception: [Bool] Flag if an exception in a thread shall be raised or just logged

    ### Returns
    Results from all `Threads` as list
    """
    if len(args) == 1:
        return list(func(arg) for arg in args)

    subprocess.Popen.communicate = partial(subprocess.Popen.communicate, timeout=30)
    with ThreadPoolExecutor(workers) as ex:
        threads = [Thread(func, arg).submit(ex) for arg in args]
    return _collect_results(threads, raise_exception)


def simultaneous(func, args, workers: int = None, raise_exception: bool = True):
    """
    Calls the given function in multiple processes for the set of given arguments
        Note that this does spawn processes, not threads. Use this for task that
        depend heavily on CPU and can be done in parallel.
    Method returns once all calls are done.

    ### Params
    - func: [Function] the function to call
    - args: [Iterable] the 'list' of arguments for each call
    - workers: [Integer] the number of concurrent threads to use (Default: NUM_CPUs)
    - raise_exception: [Bool] Flag if an exception in a thread shall be raised or just logged

    ### Returns
    Results from all `Threads` as list
    """
    if len(args) == 1:
        return list(func(arg) for arg in args)

    if workers is None:
        workers = CPU_LIM
    with ProcessPoolExecutor(workers) as ex:
        threads = [Thread(func, arg).submit(ex) for arg in args]
    return _collect_results(threads, raise_exception)


def _collect_results(threads: list, raise_exception: bool = True) -> list:
    """
    Takes a list of threads and busy waits for them to be executed.

    ### Params
    - threads: [List<Thread>] a list of submitted threads
    - raise_exception: [Bool] Flag if an exception in a thread shall be raised or just logged

    ### Returns
    Results from all `Threads` as list
    """
    result = []
    while len(threads) > 0:
        for thread in threads:
            if not thread.is_submitted():
                log.debug('Removing not submitted thread.')
                threads.remove(thread)
            if not thread.is_done():
                continue

            if thread.exception is not None:
                _exception_handling(threads, thread, raise_exception)
            else:
                result.append(thread.result)
            threads.remove(thread)
        if len(threads):
            time.sleep(0.1)
    return result


def _exception_handling(threads, thread, raise_exception):
    ex = thread.exception
    print('')
    log.critical("Execution of '%s' caused\n[%s]: %s",
                 thread.function.__name__, ex.__class__.__name__, ex)
    if raise_exception:
        # Stop all remaining threads:
        for t in threads:
            t.cancel()
        raise ex
