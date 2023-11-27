from __future__ import absolute_import

import itertools
from typing import Union


def chunks(l: list, n: int):
    for i in range(0, len(l), n):
        yield l[i:i + n]


def ichunks(iterable: Union[list, tuple], n: int):
    it = iter(iterable)
    while True:
        chunk = tuple(itertools.islice(it, n))
        if not chunk:
            return
        yield chunk
