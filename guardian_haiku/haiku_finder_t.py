# -*- coding: utf-8 -*-
"""
The Haiku Finder algorithm:

Double? pass over tokens created from tokenizer...
TODO Complete this description

"""
from typing import List

from .tokenizer import Token


def find_haiku(dictionary, tokens):

    def assign_syllable(token: Token):
        if token.type == "word":
            return token, dictionary.syllables(token.value)
        else:
            return token, None

    def assign_syllables(tokens: List[Token]):
        for token in tokens:
            yield assign_syllable(token)

    return assign_syllables(tokens)
