# -*- coding: utf-8 -*-
import logging
import nltk

logger = logging.getLogger(__name__)


class Dictionary(object):
    def __init__(self):
        try:
            logger.debug("Loading nltk's cmudict")
            self.cmu_dictionary = nltk.corpus.cmudict.dict()
        except LookupError as e:
            logger.info("Failed to load nltk's cmudict: {}".format(e))
            if not nltk.download("cmudict"):
                raise IOError("Failed to download cmudict")
            self.cmu_dictionary = nltk.corpus.cmudict.dict()

        self.cache = {}
        self.unknown_words = []

    def syllables(self, word: str) -> int:
        try:
            return self.cache[word]
        except KeyError:
            try:
                s = self.syllables_from_cmudict(word)
                self.cache[word] = s
                return s
            except KeyError:
                self.unknown_words.append(word)
                return None

    def syllables_from_cmudict(self, word: str) -> int:
        # cmudict actually returns a list of phonetics, so by default
        # choose first length
        return len([1 for syllable in self.cmu_dictionary[word.lower()][0]
                    if is_vowel_sound(syllable)])


def is_vowel_sound(syllable):
    return syllable[-1] in map(str, [1, 2, 3, 4, 5, 6, 7, 8, 9, 0])
