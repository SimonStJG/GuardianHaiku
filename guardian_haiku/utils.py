# -*- coding: utf-8 -*-
import collections


def flatten(l):
    """I know this isn't pythonic, but I don't care."""
    for x in l:
        if isinstance(x, collections.Iterable) and not isinstance(x, str):
            yield from flatten(x)
        else:
            yield x
