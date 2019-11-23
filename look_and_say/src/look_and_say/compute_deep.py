from collections import deque
from typing import List, Deque, Iterator

from .core import look_and_say, memoized_step


def brute_deep_lns(string: str, depth: int, call=look_and_say):
    """
    Simple Look-and-Say calculation at depth, by calling the base
    logic as many times as needed. Quite slow.
    """
    for _ in range(depth):
        string = call(string)
    return string


def list_deep_lns(string: str, depth: int) -> List[str]:
    """List-based Look-and-Say at a given depth"""
    if depth <= 0:
        return [string]
    atoms = [look_and_say(string)]
    for _ in range(depth - 1):
        next_atoms = []
        for string in atoms:
            next_atoms += memoized_step(string)
        atoms = next_atoms
    return atoms


def linked_deep_lns(string: str, depth: int) -> Deque[str]:
    """Deque-based Look-and-Say at a given depth"""
    if depth <= 0:
        return deque([string])
    atoms = deque([look_and_say(string)])
    for _ in range(depth - 1):
        steps = len(atoms)
        for _ in range(steps):
            atom = atoms.popleft()
            atoms.extend(memoized_step(atom))
    return atoms


def recursive_deep_lns(string: str, depth: int, top=True) -> Iterator[str]:
    """Depth-first recursive iteration of Look-and-Say"""
    if depth <= 0:
        yield string
    elif top:
        yield from recursive_deep_lns(look_and_say(string), depth - 1, False)
    else:
        for atom in memoized_step(string):
            yield from recursive_deep_lns(atom, depth - 1, False)


def stack_deep_lns(string: str, depth: int) -> Iterator[str]:
    if depth <= 0:
        yield string
        return
    stack = [[look_and_say(string)]]
    _cur_depth = 1
    while stack:
        atoms = stack.pop()
        if _cur_depth == depth:
            yield from reversed(atoms)
            _cur_depth -= 1
        elif not atoms:
            _cur_depth -= 1
        else:
            atom = atoms.pop()
            stack.append(atoms)
            stack.append(memoized_step(atom).copy())
            stack[-1].reverse()
            _cur_depth += 1
