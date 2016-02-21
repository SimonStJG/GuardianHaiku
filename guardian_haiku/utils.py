# -*- coding: utf-8 -*-
from typing import Iterator, Any


def flatten(l: Iterator[Iterator[Any]]) -> Iterator[Any]:
    """I know this isn't pythonic, but I don't care."""
    for x in l:
        yield from x
