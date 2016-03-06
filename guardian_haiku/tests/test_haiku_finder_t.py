# -*- coding: utf-8 -*-
import pytest
from guardian_haiku.dictionary import Dictionary, WordNotFoundException

from guardian_haiku.haiku_finder_t import assign_syllables
from guardian_haiku.tokenizer import Token

HAIKU = "Greedy yellow birds. Sing the muddy riverbank. On a window sill."
HYPHENATED_HAIKU = "Greedy yellow birds - Sing the muddy riverbank. " \
                   "On a window sill."
HAIKU_WITHOUT_ENDING_PUNCTUATION = \
    "Greedy yellow birds. Sing the muddy riverbank. On a window sill"
HAIKU_WITH_NONSTANDARD_SPACING = \
    "Greedy yellow birds.  Sing the muddy riverbank.  On a window sill."
SEVEN_SYLLABLE_SENTENCE = "This is a random sentence. "
FIVE_SYLLABLE_SENTENCE = "Refrigerator."
UNKNOWN_WORD = "thisIsNotAWord. "


@pytest.fixture(scope='module')
def dictionary():
    return Dictionary()


def test_assign_syllables(dictionary):
    assert list(assign_syllables(dictionary, [Token("word", "word")])) == [(Token("word", "word"), 1)]


def test_assign_syllables_for_word_not_found(dictionary):
    assert list(assign_syllables(dictionary, [Token("word", "word"),
                                              Token(" ", "whitespace"),
                                              Token("sdlh", "word")])) == [(Token("word", "word"), 1),
                                                                           (Token(" ", "whitespace"), None),
                                                                           (Token("sdlh", "word"),
                                                                            WordNotFoundException)]
