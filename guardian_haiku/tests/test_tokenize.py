# -*- coding: utf-8 -*-
from guardian_haiku.tokenizer import tokenize, Token


def test_single_word():
    assert list(tokenize("Hello")) == [Token("Hello", "word")]


def test_two_words():
    assert list(tokenize("Hello World")) == [Token("Hello", "word"),
                                             Token(" ", "whitespace"),
                                             Token("World", "word")]


def test_word_then_punctuation():
    assert list(tokenize("Hello.")) == [Token("Hello", "word"),
                                        Token(".", "punctuation")]


def test_hypenated_word():
    assert list(tokenize("Hello-world")) == [Token("Hello-world", "word")]


def test_hybrid_word_with_number():
    assert list(tokenize("Area51 blah")) == [Token("Area51", "word"),
                                             Token(" ", "whitespace"),
                                             Token("blah", "word")]


def test_number():
    assert list(tokenize("125")) == [Token("125", "digit")]


def test_number_then_punctuation():
    assert list(tokenize("125!!")) == [Token("125", "digit"),
                                       Token("!!", "punctuation")]


def test_two_numbers():
    assert list(tokenize("1 22")) == [Token("1", "digit"),
                                      Token(" ", "whitespace"),
                                      Token("22", "digit")]


def test_hybrid_number_with_word():
    assert list(tokenize("7zip")) == [Token("7zip", "word")]


def test_large_whitespace():
    assert list(tokenize("Massive gap.  Here.")) == [Token('Massive', 'word'),
                                                     Token(' ', 'whitespace'),
                                                     Token('gap', 'word'),
                                                     Token('.', 'punctuation'),
                                                     Token('  ', 'whitespace'),
                                                     Token('Here', 'word'),
                                                     Token('.', 'punctuation')]


def test_whitespace_with_punctuation():
    assert list(tokenize(".  ..  .")) == [Token('.', 'punctuation'),
                                          Token('  ', 'whitespace'),
                                          Token('..', 'punctuation'),
                                          Token('  ', 'whitespace'),
                                          Token('.', 'punctuation')]


def test_digit_and_punctuation():
    assert list(tokenize("1:02:08")) == [Token('1', 'digit'),
                                         Token(':', 'punctuation'),
                                         Token('02', 'digit'),
                                         Token(':', 'punctuation'),
                                         Token('08', 'digit')]


def test_punctuation_then_word():
    assert list(tokenize("!word")) == [Token('!', 'punctuation'),
                                       Token('word', 'word')]
