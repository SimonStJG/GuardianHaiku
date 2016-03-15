# -*- coding: utf-8 -*-
"""
Builds clauses with tokens from the tokenizer.
"""
from functools import reduce

from typing import Iterator, Generator, List

from .dictionary import logger
from .rhymeriser import rhyming_phoneme_calculator

from .tokenizer import Token, tokenize
from .utils import list_valued_dictionary

Clause = List[Token]


class DodgyClauseError(ValueError):
    pass


# TODO Add type annotations
def get_rhyming_clauses(text: str):

    # TODO Better heuristics
    def build_clauses(tokens: Iterator[Token]) -> Generator[Clause, None, None]:
        clause = []
        for token in tokens:
            clause.append(token)
            if token.type == "punctuation":
                if len(clause) > 1:
                    yield clause
                    clause = []
                else:
                    logger.error("Found a clause of length 1?  {}".format(clause))
                    clause = []
        if len(clause) > 1:
            yield clause

    def get_last_word(clause: Clause) -> str:
        for token in clause[::-1]:
            if token.type == "word":
                return token.value
        raise ValueError("Can't get last word of clause containing no words")

    with rhyming_phoneme_calculator() as rhymeriser:
        return list_valued_dictionary((rhymeriser(get_last_word(c)), c) for c in build_clauses(tokenize(text)))


# TODO This is pretty crap - it won't rebuild properly
def rebuild(clauses: List[Clause]):
    def rebuild_clause(clause: Clause):
        return reduce(lambda acc, x: acc + x.value, clause, "")

    return "".join(rebuild_clause(c) for c in clauses)


# TODO Add type annotations
def build_poem(rhyming_clauses):
    for k in rhyming_clauses.keys():
        if len(rhyming_clauses[k]) >= 2:
            return rebuild(rhyming_clauses[k][:3])


def poet(text: str) -> str:
    return build_poem(get_rhyming_clauses(text))
