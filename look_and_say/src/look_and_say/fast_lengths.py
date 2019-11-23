from collections import Counter
from functools import lru_cache
from typing import Iterator, Dict, List, Tuple

from .base import imperative_look_and_say as lns
from .cosmology import split_to_elements, make_length_iterators
from .split import split, memoized_split_lns
from .tools import parallel_iterator, iter_goto

@lru_cache(maxsize=None)
def _recursive_lns_length(string: str, depth: int) -> int:
    if depth <= 0:
        return len(string)
    return sum(
        _recursive_lns_length(atom, depth - 1)
        for atom in memoized_split_lns(string)
    )

def recursive_lns_length(string: str, depth: int) -> int:
    if depth <= 0:
        return len(string)
    return _recursive_lns_length(lns(string), depth - 1)
recursive_lns_length.cache_clear = _recursive_lns_length.cache_clear

def cached_lns_length(string: str, depth: int) -> int:
    if depth <= 0:
        return len(string)
    cache: Dict[Tuple[str, int], int] = {}
    stack: List[Tuple[str, int]] = [(lns(string), depth-1)]
    while stack:
        _str, _depth = current = stack[-1]
        if not _depth:
            cache[current] = len(_str)
            stack.pop()
            continue
        result = 0
        for atom in memoized_split_lns(_str):
            key = (atom, _depth-1)
            if key not in cache:
                stack.append(key)
                break
            result += cache[key]
        else:
            cache[current] = result
            stack.pop()
    return cache[(lns(string), depth-1)]

def stack_lns_length(string: str, depth: int) -> int:
    if depth <= 0:
        return len(string)
    cache: Dict[Tuple[str, int], int] = {}
    calls = [('get', lns(string), depth-1)]
    results = []
    while calls:
        current = calls.pop()
        op = current[0]
        if op == 'sum':
            results[-1] = results[-2] + results.pop()

        elif op == 'set':
            cache[current[1:]] = results[-1]

        else:  # get
            _str, _depth = key = current[1:]
            if _depth == 0:
                results.append(len(_str))
            elif key in cache:
                results.append(cache[key])
            else:
                calls.append(('set', _str, _depth))
                atoms = memoized_split_lns(_str)
                calls.extend([('sum',)] * (len(atoms) - 1))
                for atom in memoized_split_lns(_str):
                    calls.append(('get', atom, _depth-1))

    return results[0]

@parallel_iterator
def _iter_lengths(string: str) -> Iterator[int]:
    yield len(string)
    iterators = [_iter_lengths(s) for s in split(lns(string))]
    while True:
        yield sum(next(i) for i in iterators)

def parallel_lns_length(string: str, depth: int) -> int:
    if depth <= 0:
        return len(string)
    return iter_goto(_iter_lengths(string), depth)
parallel_lns_length.cache_clear = _iter_lengths.cache_clear

def cosmology_lns_length(string: str, depth: int):
    if depth <= 25:
        return recursive_lns_length(string, depth)
    elements = Counter(split_to_elements(string))
    ini_iterators = make_length_iterators([n for n, _ in elements])
    iterators = []
    for (elem, start), count in elements.items():
        _iter = ini_iterators[elem].pop()
        iter_goto(_iter, 25 - start)
        iterators.append((_iter, count))
    assert all(not l for l in ini_iterators.values())
    del elements, ini_iterators

    def inner():
        while True:
            yield sum(c * next(i) for i, c in iterators)

    return iter_goto(inner(), depth-26)
