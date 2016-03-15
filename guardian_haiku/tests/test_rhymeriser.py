# -*- coding: utf-8 -*-
import pytest
from guardian_haiku.rhymeriser import rhyming_phoneme_calculator


rhyming_words = [
    ("hold", "bold"),      # Differ by the last three phonemes.
    ("hold", "held"),      # Differ by only the last two phonemes
    ("sorrow", "borrow"),  # Different vowel stresses
    ("aye", "i")           # Single phoneme
]

non_rhyming_words = [
    ("pillow", "pill"),  # Same first three phonemes.
    ("aye", "oy")        # Similar, but not identical single phoneme.
]


# This one takes ages to start up, but it immutable, so make it the largest possible scope (session).
@pytest.fixture(scope="session")
def phonemiser():
    with rhyming_phoneme_calculator() as phonemiser:
        return phonemiser


@pytest.mark.parametrize("lhs,rhs", rhyming_words)
def test_rhyming_words(lhs, rhs, phonemiser):
    import pprint
    assert phonemiser(lhs) == phonemiser(rhs), pprint.pformat((lhs, rhs))


@pytest.mark.parametrize("lhs,rhs", non_rhyming_words)
def test_non_rhyming_words(lhs, rhs, phonemiser):
    assert phonemiser(lhs) != phonemiser(rhs)
