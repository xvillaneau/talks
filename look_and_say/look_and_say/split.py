from functools import lru_cache
import re
from typing import List, Iterator

from .base import imperative_look_and_say

__all__ = ('split', 'memoized_split_lns')

# Splitting a sequence
RE_ENDSPLIT = re.compile(r'[^2]22$')
RE_SPLITS = [
    re.compile(r'21([^1])(?!\1)'),
    re.compile(r'2111[^1]'),
    re.compile(r'23(?:$|([^3]){1,2}(?!\1))'),
    re.compile(r'2([^123])(?!\1)'),
    re.compile(r'[^123][123]'),
]

def split(string: str) -> List[str]:
    return list(_split(string))

def _split(string: str) -> Iterator[str]:
    if string == '22':
        yield string
    elif RE_ENDSPLIT.search(string):
        yield from _split(string[:-2])
        yield '22'
    else:
        for regex in RE_SPLITS:
            if match := regex.search(string):
                p = match.start() + 1
                yield from _split(string[:p])
                yield from _split(string[p:])
                return
        yield string

@lru_cache(maxsize=None)
def memoized_split_lns(string: str) -> List[str]:
    """
    Memoized version of Look-and-Say that also splits the result.

    IMPORTANT: DO NOT APPLY ON INPUT STRINGS! The Splitting Theorem
    only works after two Look-and-Say iterations!
    """
    return split(imperative_look_and_say(string))
