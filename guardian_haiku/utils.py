# -*- coding: utf-8 -*-
from functools import reduce


def flatten(l):
    """I know this isn't pythonic, but I don't care."""
    return reduce(lambda x, xs: x + xs, l, [])
