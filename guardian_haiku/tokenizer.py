# -*- coding: utf-8 -*-
from collections import namedtuple
from typing import Generator
from more_itertools import peekable

Token = namedtuple("token", ("value", "type"))


def tokenize(paragraph: str) -> Generator[Token, None, None]:
    x = _tokenize(paragraph)
    # We ignore the first element yielded from _tokenize because it's either ("", "whitespace") or, if there was some
    # other whitespace at the beginning of the string, it'll be that.
    next(x)
    yield from x


def _tokenize(paragraph: str) -> Generator[Token, None, None]:
    paragraph = peekable(paragraph)
    acc = ""
    acc_type = "whitespace"  # Start from whitespace, because it gives the right results.
    for char in paragraph:
        char_type = get_char_type(char)

        # Odd special-case behaviours.
        #
        if acc_type == "word" and char_type == "punctuation":
            next_type = get_char_type(paragraph.peek(default=" "))  # TODO This is a bit hack-y
            if next_type == "word":  # If it's sandwiched between two chars, it's probably ' or - or similar.
                acc += char
            else:
                yield Token(acc, acc_type)
                acc = char
                acc_type = "punctuation"
            continue
        if acc_type == "word" and char_type == "digit":  # This is pretty weird, treat it as a word.
            acc += char
            continue
        if acc_type == "digit" and char_type == "word":  # This is pretty weird, treat it as a word.
            acc += char
            acc_type = "word"
            continue

        # Default behaviours
        #
        if char_type == acc_type:
            acc += char
        else:
            yield Token(acc, acc_type)
            acc = char
            acc_type = char_type

    yield Token(acc, acc_type)


def get_char_type(char: str) -> str:
    assert len(char) == 1
    if char.isalpha():
        return "word"
    elif char.isdigit():
        return "digit"
    elif char.isspace():
        return "whitespace"
    else:
        return "punctuation"


class ParseError(Exception):
    pass
