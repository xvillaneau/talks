from collections import deque
from typing import List, Deque, Iterator

from .base import imperative_look_and_say as lns
from .split import memoized_split_lns

def list_deep_lns(string: str, depth: int) -> List[str]:
    """List-based Look-and-Say at a given depth"""
    if depth <= 0:
        return [string]
    atoms = [lns(string)]
    for _ in range(depth-1):
        next_atoms = []
        for string in atoms:
            next_atoms.extend(memoized_split_lns(string))
        atoms = next_atoms
    return atoms

def linked_deep_lns(string: str, depth: int) -> Deque[str]:
    """Deque-based Look-and-Say at a given depth"""
    if depth <= 0:
        return deque([string])
    atoms = deque([lns(string)])
    for _ in range(depth-1):
        steps = len(atoms)
        for _ in range(steps):
            atom = atoms.popleft()
            atoms.extend(memoized_split_lns(atom))
    return atoms

def recursive_deep_lns(string: str, depth: int, top=True) -> Iterator[str]:
    """Depth-first recursive iteration of Look-and-Say"""
    if depth <= 0:
        yield string
    elif top:
        yield from recursive_deep_lns(lns(string), depth - 1, False)
    else:
        for atom in memoized_split_lns(string):
            yield from recursive_deep_lns(atom, depth - 1, False)

def stack_deep_lns(string: str, depth: int) -> Iterator[str]:
    if depth <= 0:
        yield string
        return
    stack = [[lns(string)]]
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
            stack.append(memoized_split_lns(atom).copy())
            stack[-1].reverse()
            _cur_depth += 1
