# -*- coding: utf-8 -*-
from typing import TypeVar, Iterator, Tuple, Dict, Set

S, T = TypeVar('S'), TypeVar('T')


# TODO Make this a subclass of dict.
def list_valued_dictionary(l: Iterator[Tuple[S, T]]) -> Dict[S, Set[T]]:
    d = {}
    for k, v in l:
        if k not in d:
            d[k] = []
        d[k].append(v)
    return d
