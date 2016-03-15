# -*- coding: utf-8 -*-
import pytest
from guardian_haiku.the_poets_brain import get_rhyming_clauses, poet
from guardian_haiku.tokenizer import Token


rhyming_clauses = [
    ("Hello World", {
        ('L', 'D'): [
            [
                Token(value='Hello', type='word'),
                Token(value=' ', type='whitespace'),
                Token(value='World', type='word')
            ]
        ]
    }),
    ("Hello World, bellow hold.", {
        ('L', 'D'): [
            [
                Token(value='Hello', type='word'),
                Token(value=' ', type='whitespace'),
                Token(value='World', type='word'),
                Token(value=',', type='punctuation')
            ], [
                Token(value=' ', type='whitespace'),
                Token(value='bellow', type='word'),
                Token(value=' ', type='whitespace'),
                Token(value='hold', type='word'),
                Token(value='.', type='punctuation')
            ]
        ]
    })
]


# TODO This test would be quicker if we could inject the cmudict.
# TODO Needs more tests.
@pytest.mark.parametrize("lhs,rhs", rhyming_clauses)
def test_get_rhyming_clauses(lhs, rhs):
    assert get_rhyming_clauses(lhs) == rhs


def test_poet():
    assert poet("Hello World, bellow hold.") == "Hello World, bellow hold."
