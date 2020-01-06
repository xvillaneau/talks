from collections import Counter, defaultdict
from itertools import tee
from pathlib import Path
import re
from typing import List, Tuple, Dict, Iterator

from .core import look_and_say, memoized_step

_elements_file = Path(__file__).parent / "elements.txt"
with open(_elements_file) as f:
    ELEMENTS = set(map(str.strip, f.readlines())) - {""}


def split_to_elements(string: str) -> List[Tuple[str, int]]:
    # Special cases for days 0 and 1
    if string in ELEMENTS:
        return [(string, 0)]
    day_1 = look_and_say(string)
    if day_1 in ELEMENTS:
        return [(day_1, 1)]

    # Day 2 onwards: replace >=4 digits by N, this allows us to
    # manipulate 2 Neptunium/Plutonium elements instead of 2 per digit.
    day_2 = re.sub("[4-9]", "N", look_and_say(day_1))

    def _rec_split(_string, depth):
        if _string in ELEMENTS:
            yield _string, depth
            return
        for atom in memoized_step(_string):
            yield from _rec_split(atom, depth + 1)

    return list(_rec_split(day_2, 2))


def make_length_iterators(
    strings: List[str]
) -> Dict[str, List[Iterator[int]]]:
    # Step 1: Count how many iterators to create for each element
    reservations = defaultdict(int)
    reservations.update(Counter(strings))
    for string in ELEMENTS:
        for atom in memoized_step(string):
            reservations[atom] += 1

    def root_iterator(_str: str, sub_iterators: List[Iterator[int]]):
        yield len(_str)
        while True:
            val = 0
            for _iter in sub_iterators:
                val += next(_iter)
            yield val

    # Step 2: Create all the iterators; one root per elements,
    # forked as many times as required.
    roots, forks = {}, {}

    for string in ELEMENTS:
        roots[string] = []
        root = root_iterator(string, roots[string])
        forks[string] = list(tee(root, reservations[string]))

    # Step 3: Send back the reserved iterators to their parents

    for string in ELEMENTS:
        for child in memoized_step(string):
            roots[string].append(forks[child].pop())

    # The remaining iterators should be the ones we asked for
    return {string: view for string, view in forks.items() if view}
