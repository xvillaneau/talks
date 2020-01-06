from collections import Counter
from functools import lru_cache
from typing import Iterator

from .core import look_and_say, memoized_step
from .cosmology import split_to_elements, make_length_iterators
from .tools import parallel_iterator, iter_goto


@lru_cache(maxsize=2048)
def _recursive_lns_length(string: str, depth: int) -> int:
    if depth <= 0:
        return len(string)
    res, n_depth = 0, depth - 1
    for atom in memoized_step(string):
        res += _recursive_lns_length(atom, n_depth)
    return res


def recursive_lns_length_iter(string: str) -> Iterator[int]:
    yield len(string)
    i, string = 0, look_and_say(string)
    while True:
        yield _recursive_lns_length(string, i)
        i += 1


def recursive_lns_length(string: str, depth: int) -> int:
    return iter_goto(recursive_lns_length_iter(string), depth)


recursive_lns_length.cache_clear = _recursive_lns_length.cache_clear


@parallel_iterator
def _iter_lengths(string: str) -> Iterator[int]:
    yield len(string)
    iterators = [_iter_lengths(s) for s in memoized_step(string)]
    while True:
        yield sum(next(i) for i in iterators)


def parallel_lns_length(string: str, depth: int) -> int:
    if depth <= 0:
        return len(string)
    return iter_goto(_iter_lengths(string), depth)


parallel_lns_length.cache_clear = _iter_lengths.cache_clear


def _cosmology_lns_length_iter(string: str):
    elements = Counter(split_to_elements(string))
    ini_iterators = make_length_iterators([n for n, _ in elements])
    iterators = []

    for (elem, start), _count in elements.items():
        _iter = ini_iterators[elem].pop()
        iter_goto(_iter, 23 - start)
        iterators.append((_iter, _count))

    if any(ini_iterators.values()):
        raise RuntimeError()
    del elements, ini_iterators

    while True:
        yield sum(c * next(i) for i, c in iterators)


def cosmology_lns_length(string: str, depth: int):
    if depth < 24:
        return recursive_lns_length(string, depth)
    return iter_goto(_cosmology_lns_length_iter(string), depth - 24)
