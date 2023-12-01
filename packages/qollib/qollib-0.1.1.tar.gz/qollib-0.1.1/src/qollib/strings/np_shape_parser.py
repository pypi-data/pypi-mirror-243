from typing import Union


def parse_shape(string: str) -> tuple:
    """
    Parses a numpy like shape string, e.g. [0:,42:1337]
    :returns: a tuple of slices that can be used with numpy arrays
    """
    string = string.strip("[]")
    return tuple(to_slice(d) if ':' in d else to_int(d) for d in string.split(","))


def to_slice(string: str, delimiter: str = ':') -> slice:
    """:returns: a slice with start and stop taken from the string, seperated by delimiter, e.g. 3:7"""
    start, stop = string.split(delimiter)
    return slice(to_int(start), to_int(stop))


def to_int(string: str) -> Union[int, None]:
    """:returns: an integer if the string is numeric"""
    if string.strip().isnumeric():
        return int(string)
    return None


def shape_slices_to_string(shape: tuple) -> str:
    out = []
    for dim in shape:
        if isinstance(dim, slice):
            out.append(f'{dim.start}:{dim.stop}')
        else:
            out.append(str(dim))
    return f"[{', '.join(out)}]"
