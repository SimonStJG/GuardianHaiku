# -*- coding: utf-8 -*-
from typing import Generator, Tuple
from more_itertools import peekable


def tokenize(paragraph: str) -> Generator[Tuple[str, str], None, None]:
    x = _tokenize(paragraph)
    # We ignore the first element yielded from _tokenize because it's either ("", "whitespace") or, if there was some
    # other whitespace at the beginning of the string, it'll be that.
    next(x)
    yield from x


def _tokenize(paragraph: str) -> Generator[Tuple[str, str], None, None]:
    paragraph = peekable(paragraph)
    acc = ""
    acc_type = "whitespace"  # Start from whitespace, because it gives the right results.
    for char in paragraph:
        t = char_type(char)
        if acc_type == "word":
            if t == "word":
                acc += char
            elif t == "punctuation":
                next_type = char_type(paragraph.peek(default=" "))  # TODO This is a bit hack-y
                if next_type == "word":  # If it's sandwiched between two chars, it's probably ' or - or similar.
                    acc += char
                else:
                    yield (acc, acc_type)
                    acc = char
                    acc_type = "punctuation"
            elif t == "digit":  # This is pretty weird, treat it as a word.
                acc += char
            elif t == "whitespace":
                yield (acc, acc_type)
                acc = char
                acc_type = "whitespace"
            else:
                raise ParseError()
        elif acc_type == "digit":
            if t == "word":  # This is pretty weird, treat it as a word.
                acc += char
                acc_type = "word"
            elif t == "digit":
                acc += char
            elif t == "whitespace":
                yield (acc, acc_type)
                acc = char
                acc_type = "whitespace"
            elif t == "punctuation":
                yield (acc, acc_type)
                acc = char
                acc_type = "punctuation"
            else:
                raise ParseError()
        elif acc_type == "whitespace":
            if t == "word":
                yield (acc, acc_type)
                acc = char
                acc_type = "word"
            elif t == "digit":
                yield (acc, acc_type)
                acc = char
                acc_type = "digit"
            elif t == "whitespace":
                acc += char
            elif t == "punctuation":
                yield (acc, acc_type)
                acc = char
                acc_type = "punctuation"
            else:
                raise ParseError()
        elif acc_type == "punctuation":
            if t == "word":  # This is an odd one.  Ignore it and start a new word.
                yield (acc, acc_type)
                acc = char
                acc_type = "word"
            elif t == "digit":
                yield (acc, acc_type)
                acc = char
                acc_type = "digit"
            elif t == "whitespace":
                yield (acc, acc_type)
                acc = char
                acc_type = "whitespace"
            elif t == "punctuation":
                acc += char
            else:
                raise ParseError()
        else:
            raise ParseError()
    yield (acc, acc_type)


def char_type(char: str) -> str:
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
