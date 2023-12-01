#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The `chunking` utility provides methods to break huge collections in chunks

@author: hoelken
"""


def chunker(seq: list, size: int) -> list:
    """
    Generates chunks (slices) from a given sequence

    ### Params
    - seq: the list to chunk
    - size: the size of the chunks

    ### Returns
    A list of lists where each list has the
        length of the requested chunk size (maybe except the last one)
    """
    if size < 1:
        return [seq]
    return [seq[pos:pos + size] for pos in range(0, len(seq), size)]


def indexed_chunks(seq: list, size: int) -> dict:
    """
    Generates indexed chunks (slices) from a given sequence
    ### Params
    - seq: List the list to chunk
    - size: Integer the size of the chunks

    ### Returns
     A dictionary with the index as key and the corresponding chunk as value.
        The length of the value arrays is the requested chunk size (maybe except the last one)
    """
    idx = 0
    indexed = {}
    for chunk in chunker(seq, size):
        indexed[idx] = chunk
        idx += 1
    return indexed
