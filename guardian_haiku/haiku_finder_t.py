# -*- coding: utf-8 -*-
"""
The Haiku Finder algorithm:

Single pass over tokens created from tokenizer...
TODO Complete this description
"""
from typing import List, Tuple, Generator

from .dictionary import WordNotFoundException, Dictionary
from .tokenizer import Token


def assign_syllables(dictionary: Dictionary,
                     tokens: List[Token]) -> Generator[Tuple[Token, int], None, None]:

    def assign_syllable(token: Token) -> Tuple[Token, int]:
        if token.type == "word":
            # If you throw in a generator, it exits.
            # TODO Should rewrite without the raise for speed.
            try:
                return token, dictionary.syllables(token.value)
            except WordNotFoundException:
                return token, WordNotFoundException
        else:
            return token, None

    for token in tokens:
        yield assign_syllable(token)


def find_haiku(dictionary: Dictionary, tokens: List[Token]) -> List[str]:

    def valid(p):
        pass

    def process(possibilities, token):
        for p in possibilities:
            p.append(token)
            if valid(p):
                yield p

    possibilities = []
    for token in tokens:
        # Completely ignore whitespace
        possibilities = list(process(possibilities, token))
