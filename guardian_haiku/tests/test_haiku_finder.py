# -*- coding: utf-8 -*-
import logging
import pytest

from guardian_haiku.haiku_finder import HaikuFinder, Word

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


logger = logging.getLogger(__name__)


def test_paragraphs():
    assert HaikuFinder().find_haiku("{}\n{}".format(HAIKU, HAIKU)) == [HAIKU] * 2


def test_no_haiku():
    assert HaikuFinder().find_haiku(SEVEN_SYLLABLE_SENTENCE + UNKNOWN_WORD) == []


def test_finds_haiku():
    assert HaikuFinder().find_haiku(HAIKU) == [HAIKU]


@pytest.mark.xfail
def test_finds_hyphenated_haiku():
    assert HaikuFinder().find_haiku(HYPHENATED_HAIKU) == [HAIKU]


def test_finds_three_haikus():
    found = HaikuFinder().find_haiku(HAIKU + SEVEN_SYLLABLE_SENTENCE + FIVE_SYLLABLE_SENTENCE + UNKNOWN_WORD + HAIKU)
    assert (found ==
            [HAIKU,
             "On a window sill. " +
             SEVEN_SYLLABLE_SENTENCE +
             FIVE_SYLLABLE_SENTENCE,
             HAIKU])


def test_finds_haiku_without_ending_punctuation():
    assert (HaikuFinder().find_haiku(HAIKU_WITHOUT_ENDING_PUNCTUATION) == [HAIKU_WITHOUT_ENDING_PUNCTUATION])


def test_unknown_word_is_ignored_at_beginning():
    assert HaikuFinder().find_haiku(UNKNOWN_WORD + HAIKU) == [HAIKU]


def test_unknown_word_is_ignored_at_end():
    assert HaikuFinder().find_haiku(HAIKU + UNKNOWN_WORD) == [HAIKU]


def test_unknown_word_triggers_callback():
    argument_captor = []

    def callback(word):
        logger.debug("Captured")
        argument_captor.append(word)

    hf = HaikuFinder(custom_dictionary=None,
                     unknown_word_callback=callback)
    hf.find_haiku("unknownword")
    assert argument_captor == ["unknownword"]


def test_custom_dictionary():
    custom_dictionary = {"customword": 6}
    word = Word("customword", {"custom_dictionary": custom_dictionary})
    assert word.syllables == 6


def test_hyphenation():
    assert Word("boom-box").syllables == 2
