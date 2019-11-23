from functools import lru_cache
from itertools import groupby
import re
from typing import List, Iterator

__all__ = (
    "imperative_look_and_say",
    "regex_look_and_say",
    "groupby_look_and_say",
    "look_and_say",
    "split",
    "memoized_step",
)

# "manual" computation of Look and Say, with a for loop
def imperative_look_and_say(string: str):
    """'Direct' implementation of the Look-and-Say logic"""
    result, times, repeat = "", 1, string[0]
    for char in string[1:]:
        if char != repeat:
            result += str(times) + repeat
            times, repeat = 1, char
        else:
            times += 1
    result += str(times) + repeat
    return result


# RegEx computation of Look and Say
RE_LNS = re.compile(r"((.)\2*)")


def regex_look_and_say(string: str):
    """RegEx-based Look-and-Say logic"""
    return "".join(str(len(g)) + g[0] for g, _ in RE_LNS.findall(string))


# Itertools-based approach
def groupby_look_and_say(string: str):
    """itertools-based Look-and-Say logic"""
    return "".join(str(len(list(g))) + k for k, g in groupby(string))


# Use the loop approach as the official implementation,
# since it's the fastest by far.
look_and_say = imperative_look_and_say

# Splitting a sequence
RE_ENDSPLIT = re.compile(r"[^2]22$")
RE_SPLITS = [
    re.compile(r"21([^1])(?!\1)"),
    re.compile(r"2111[^1]"),
    re.compile(r"23(?:$|([^3]){1,2}(?!\1))"),
    re.compile(r"2([^123])(?!\1)"),
    re.compile(r"[^123][123]"),
]


def split(string: str) -> List[str]:
    """
    Split a string, as described in Conway's Splitting Theorem.

    IMPORTANT: DO NOT APPLY TO zero-day or one-day strings!
    """
    return list(_split(string))


def _split(string: str) -> Iterator[str]:
    """Internal recursive generator for splitting"""
    if string == "22":
        yield string
    elif RE_ENDSPLIT.search(string):
        yield from _split(string[:-2])
        yield "22"
    else:
        for regex in RE_SPLITS:
            match = regex.search(string)
            if match:
                p = match.start() + 1
                yield from _split(string[:p])
                yield from _split(string[p:])
                return
        yield string


@lru_cache(maxsize=128)
def memoized_step(string: str) -> List[str]:
    """
    Memoized version of Look-and-Say that also splits the result.

    IMPORTANT: DO NOT APPLY ON INPUT STRINGS! The Splitting Theorem
    only works after two Look-and-Say iterations!
    """
    return split(look_and_say(string))
