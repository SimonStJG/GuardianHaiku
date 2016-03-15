# -*- coding: utf-8 -*-
"""
Use rhyming_phoneme_calculator to tell if two words rhyme with each other.
"""
from contextlib import contextmanager
import logging
from typing import List, Dict
import nltk

logger = logging.getLogger(__name__)


class UnknownWordException(ValueError):
    def __init__(self, word):
        super(UnknownWordException).__init__("{} not present in the Carnegie Mellon University dictionary".format(word))


def load_or_download_cmudict():
    """Download Carnegie Mellon University's Pronunciation dictionary"""
    try:
        logger.debug("Attempting to load nltk's cmudict")
        return nltk.corpus.cmudict.dict()
    except LookupError:
        logger.exception("Failed to load nltk's cmudict, attempting to download it")
        if not nltk.download("cmudict"):
            raise IOError("Failed to download cmudict")
        return nltk.corpus.cmudict.dict()


# TODO Complete type annotations
def get_rhyming_phonemes(word: str,
                         cmudict: Dict[str, List[List[str]]]):
    """
    I'm defining (because I say so), the "rhyming phonemes" of a word to be the last two phonemes, with any stress
    indication removed from the vowel sounds.  If the word is only a single phoneme long, then the "rhyming phonemes" of
    that word is just that syllable.

    This seems to give a pretty solid indication of which words will rhyme.  Although sometimes the first pronunciation
    returned by the dictionary is not what I'd call the standard one.  But who am I to say what is the standard
    pronunciation.
    """
    def strip_stress_suffix(phoneme: str) -> str:
        if phoneme[-1].isdigit():
            return phoneme[:-1]
        else:
            return phoneme

    try:
        # The cmudict returns a list of possible pronunciations, each pronunciation is a list of phonemes.  The
        # vowels are additionally marked for stress with a suffix of 1, 2, or 3.  eg.
        # cmudict["hello"] = [['HH', 'AH0', 'L', 'OW1'], ['HH', 'EH0', 'L', 'OW1']]
        pronunciation = cmudict[word][0]
    except KeyError:
        raise UnknownWordException(word)

    try:
        key_phonemes = tuple(pronunciation[-2:])
    except IndexError:
        key_phonemes = tuple(pronunciation[-1:])

    return tuple(strip_stress_suffix(kp) for kp in key_phonemes)


@contextmanager
def rhyming_phoneme_calculator():
    cmudict = load_or_download_cmudict()
    cache = {}

    def f(word: str) -> List[str]:
        word = word.lower()
        try:
            return cache[word]
        except KeyError:
            rhyming_phonemes = get_rhyming_phonemes(word, cmudict)
            cache[word] = rhyming_phonemes
            return rhyming_phonemes

    yield f
