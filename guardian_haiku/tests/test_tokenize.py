# -*- coding: utf-8 -*-
from guardian_haiku.tokenizer import tokenize


def test_single_word():
    assert list(tokenize("Hello")) == [("Hello", "word")]


def test_two_words():
    assert list(tokenize("Hello World")) == [("Hello", "word"), (" ", "whitespace"), ("World", "word")]


def test_word_then_punctuation():
    assert list(tokenize("Hello.")) == [("Hello", "word"), (".", "punctuation")]


def test_hypenated_word():
    assert list(tokenize("Hello-world")) == [("Hello-world", "word")]


def test_hybrid_word_with_number():
    assert list(tokenize("Area51 blah")) == [("Area51", "word"), (" ", "whitespace"), ("blah", "word")]


def test_number():
    assert list(tokenize("125")) == [("125", "digit")]


def test_number_then_punctuation():
    assert list(tokenize("125!!")) == [("125", "digit"), ("!!", "punctuation")]


def test_two_numbers():
    assert list(tokenize("1 22")) == [("1", "digit"), (" ", "whitespace"), ("22", "digit")]


def test_hybrid_number_with_word():
    assert list(tokenize("7zip")) == [("7zip", "word")]


def test_large_whitespace():
    assert list(tokenize("Massive gap.  Here.")) == [('Massive', 'word'),
                                                     (' ', 'whitespace'),
                                                     ('gap', 'word'),
                                                     ('.', 'punctuation'),
                                                     ('  ', 'whitespace'),
                                                     ('Here', 'word'),
                                                     ('.', 'punctuation')]


def test_whitespace_with_punctuation():
    assert list(tokenize(".  ..  .")) == [('.', 'punctuation'),
                                          ('  ', 'whitespace'),
                                          ('..', 'punctuation'),
                                          ('  ', 'whitespace'),
                                          ('.', 'punctuation')]


def test_digit_and_punctuation():
    assert list(tokenize("1:02:08")) == [('1', 'digit'),
                                         (':', 'punctuation'),
                                         ('02', 'digit'),
                                         (':', 'punctuation'),
                                         ('08', 'digit')]


def test_punctuation_then_word():
    assert list(tokenize("!word")) == [('!', 'punctuation'),
                                       ('word', 'word')]
