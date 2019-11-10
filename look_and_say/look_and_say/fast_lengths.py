from itertools import islice, tee, count
from functools import wraps, lru_cache
from typing import Iterator, Dict, List, Tuple

from .split import split, memoized_split_lns
from .base import imperative_look_and_say as lns

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
        _str, _depth = current = stack.pop()
        if _depth == 0:
            cache[current] = len(_str)
            continue
        result = 0
        for atom in memoized_split_lns(_str):
            key = (atom, _depth-1)
            if key not in cache:
                stack.extend([current, key])
                break
            result += cache[key]
        else:
            cache[current] = result
    return cache[(lns(string), depth-1)]

def parallel_iterator(generator_func):
    roots = {}

    @wraps(generator_func)
    def inner(*args):
        if args not in roots:
            roots[args] = generator_func(*args)
        iterator, roots[args] = tee(roots[args], 2)
        return iterator

    inner.cache_clear = roots.clear
    return inner

@parallel_iterator
def _iter_lengths(string: str) -> Iterator[int]:
    yield len(string)
    iterators = [_iter_lengths(s) for s in split(lns(string))]
    while True:
        yield sum(next(i) for i in iterators)

def parallel_lns_length(string: str, depth: int) -> int:
    if depth <= 0:
        return len(string)
    return next(islice(_iter_lengths(string), depth, None))
parallel_lns_length.cache_clear = _iter_lengths.cache_clear
