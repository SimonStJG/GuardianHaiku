# -*- coding: utf-8 -*-
"""
Use nltk to find haiku in text.
"""
import logging
from functools import lru_cache
from typing import List
from guardian_haiku.dictionary import WordNotFoundException, Dictionary


logger = logging.getLogger(__name__)


def find_haiku(paragraph: str,
               dictionary)-> List[str]:  # TODO SJG Remove default, fix tests
    clauses = split_into_clauses(paragraph, dictionary)
    return find_haiku_in_clauses(clauses)


def split_into_clauses(paragraph: str, dictionary: Dictionary) -> List[str]:
    clauses = []
    next_clause_starting_position = 0
    for i, char in enumerate(paragraph):
        if not (char.isalpha() or char == ' '):
            clause = paragraph[next_clause_starting_position:i].strip()
            if clause:
                clauses.append(Clause(clause, char, dictionary))
            next_clause_starting_position = i + 1

    final_clause = paragraph[next_clause_starting_position:].strip()
    if final_clause:
        clauses.append(Clause(final_clause, '', dictionary))

    return clauses


def find_haiku_in_clauses(clauses):
    logger.debug("Finding haiku in {}".format(clauses))
    haiku_found = []
    syllable_lengths = [x.syllables for x in clauses]
    for i in range(0, len(clauses) - 2):
        if syllable_lengths[i:i+3] == [5, 7, 5]:
            haiku_found.append(" ".join(
                [x.full_text for x in clauses[i:i+3]]))

    return haiku_found


class Clause(object):
    def __init__(self, text, ending_punctuation, dictionary):
        self._text = text
        self._ending_punctuation = ending_punctuation
        self._dictionary = dictionary

    @property
    @lru_cache()
    def syllables(self):
        try:
            return sum([self._dictionary.syllables(word) for word in self._text.split()])
        except WordNotFoundException:
            return None

    @property
    @lru_cache()
    def full_text(self):
        return self._text + self._ending_punctuation

    def __repr__(self):
        return "Clause: {}({})".format(self.full_text, self.syllables)
