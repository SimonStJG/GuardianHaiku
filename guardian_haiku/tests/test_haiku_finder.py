# -*- coding: utf-8 -*-
import pytest
from guardian_haiku.dictionary import Dictionary

from guardian_haiku.haiku_finder import find_haiku

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


def test_paragraphs(dictionary):
    assert find_haiku("{}\n{}".format(HAIKU, HAIKU), dictionary) == [HAIKU] * 2


def test_no_haiku(dictionary):
    assert find_haiku(SEVEN_SYLLABLE_SENTENCE + UNKNOWN_WORD, dictionary) == []


def test_finds_haiku(dictionary):
    assert find_haiku(HAIKU, dictionary) == [HAIKU]


@pytest.mark.xfail
def test_finds_hyphenated_haiku(dictionary):
    assert find_haiku(HYPHENATED_HAIKU, dictionary) == [HAIKU]


def test_finds_three_haikus(dictionary):
    found = find_haiku(HAIKU + SEVEN_SYLLABLE_SENTENCE + FIVE_SYLLABLE_SENTENCE + UNKNOWN_WORD + HAIKU, dictionary)
    assert (found ==
            [HAIKU,
             "On a window sill. " +
             SEVEN_SYLLABLE_SENTENCE +
             FIVE_SYLLABLE_SENTENCE,
             HAIKU])


def test_finds_haiku_without_ending_punctuation(dictionary):
    assert find_haiku(HAIKU_WITHOUT_ENDING_PUNCTUATION, dictionary) == [HAIKU_WITHOUT_ENDING_PUNCTUATION]


def test_unknown_word_is_ignored_at_beginning(dictionary):
    assert find_haiku(UNKNOWN_WORD + HAIKU, dictionary) == [HAIKU]


def test_unknown_word_is_ignored_at_end(dictionary):
    assert find_haiku(HAIKU + UNKNOWN_WORD, dictionary) == [HAIKU]


# def test_hyphenation():
#     assert Word("boom-box").syllables == 2
