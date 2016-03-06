# -*- coding: utf-8 -*-
import pytest
from guardian_haiku.dictionary import Dictionary

from guardian_haiku.haiku_finder_t import find_haiku
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
    assert list(find_haiku(dictionary, [Token("word", "word")])) == [(Token("word", "word"), 1)]