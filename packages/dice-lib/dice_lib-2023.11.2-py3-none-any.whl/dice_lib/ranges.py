from itertools import count
from typing import Iterable, Iterator


def as_range(iterable: Iterable[int]) -> str:
    """From https://codereview.stackexchange.com/q/5196
    If {iterable} has at least two elements, return '{first}-{last}', otherwise '{first}'.
    """
    items = list(iterable)
    if len(items) > 1:
        return f"{items[0]}-{items[-1]}"
    else:
        return f"{items[0]}"


def groupby_range(x: int, c: Iterator[int] = count()) -> int:
    return next(c) - x


def groupby_inverse_range(x: int, c: Iterator[int] = count()) -> int:
    return x - next(c)
