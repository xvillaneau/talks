from collections import Counter
from itertools import tee
import re
from typing import List, Tuple, Dict, Iterator

from .base import imperative_look_and_say as lns
from .split import memoized_split_lns

COSMOLOGY: Dict[str, Tuple[str, List[str]]] = {
    "H": ('22', ["H"]),
    "He": ('13112221133211322112211213322112', ["Hf", "Pa", "H", "Ca", "Li"]),
    "Li": ('312211322212221121123222112', ["He"]),
    "Be": ('111312211312113221133211322112211213322112', ["Ge", "Ca", "Li"]),
    "B": ('1321132122211322212221121123222112', ["Be"]),
    "C": ('3113112211322112211213322112', ["B"]),
    "N": ('111312212221121123222112', ["C"]),
    "O": ('132112211213322112', ["N"]),
    "F": ('31121123222112', ["O"]),
    "Ne": ('111213322112', ["F"]),
    "Na": ('123222112', ["Ne"]),
    "Mg": ('3113322112', ["Pm", "Na"]),
    "Al": ('1113222112', ["Mg"]),
    "Si": ('1322112', ["Al"]),
    "P": ('311311222112', ["Ho", "Si"]),
    "S": ('1113122112', ["P"]),
    "Cl": ('132112', ["S"]),
    "Ar": ('3112', ["Cl"]),
    "K": ('1112', ["Ar"]),
    "Ca": ('12', ["K"]),
    "Sc": ('3113112221133112', ["Ho", "Pa", "H", "Ca", "Co"]),
    "Ti": ('11131221131112', ["Sc"]),
    "V": ('13211312', ["Ti"]),
    "Cr": ('31132', ["V"]),
    "Mn": ('111311222112', ["Cr", "Si"]),
    "Fe": ('13122112', ["Mn"]),
    "Co": ('32112', ["Fe"]),
    "Ni": ('11133112', ["Zn", "Co"]),
    "Cu": ('131112', ["Ni"]),
    "Zn": ('312', ["Cu"]),
    "Ga": ('13221133122211332', ["Eu", "Ca", "Ac", "H", "Ca", "Zn"]),
    "Ge": ('31131122211311122113222', ["Ho", "Ga"]),
    "As": ('11131221131211322113322112', ["Ge", "Na"]),
    "Se": ('13211321222113222112', ["As"]),
    "Br": ('3113112211322112', ["Se"]),
    "Kr": ('11131221222112', ["Br"]),
    "Rb": ('1321122112', ["Kr"]),
    "Sr": ('3112112', ["Rb"]),
    "Y": ('1112133', ["Sr", "U"]),
    "Zr": ('12322211331222113112211', ["Y", "H", "Ca", "Tc"]),
    "Nb": ('1113122113322113111221131221', ["Er", "Zr"]),
    "Mo": ('13211322211312113211', ["Nb"]),
    "Tc": ('311322113212221', ["Mo"]),
    "Ru": ('132211331222113112211', ["Eu", "Ca", "Tc"]),
    "Rh": ('311311222113111221131221', ["Ho", "Ru"]),
    "Pd": ('111312211312113211', ["Rh"]),
    "Ag": ('132113212221', ["Pd"]),
    "Cd": ('3113112211', ["Ag"]),
    "In": ('11131221', ["Cd"]),
    "Sn": ('13211', ["In"]),
    "Sb": ('3112221', ["Pm", "Sn"]),
    "Te": ('1322113312211', ["Eu", "Ca", "Sb"]),
    "I": ('311311222113111221', ["Ho", "Te"]),
    "Xe": ('11131221131211', ["I"]),
    "Cs": ('13211321', ["Xe"]),
    "Ba": ('311311', ["Cs"]),
    "La": ('11131', ["Ba"]),
    "Ce": ('1321133112', ["La", "H", "Ca", "Co"]),
    "Pr": ('31131112', ["Ce"]),
    "Nd": ('111312', ["Pr"]),
    "Pm": ('132', ["Nd"]),
    "Sm": ('311332', ["Pm", "Ca", "Zn"]),
    "Eu": ('1113222', ["Sm"]),
    "Gd": ('13221133112', ["Eu", "Ca", "Co"]),
    "Tb": ('3113112221131112', ["Ho", "Gd"]),
    "Dy": ('111312211312', ["Tb"]),
    "Ho": ('1321132', ["Dy"]),
    "Er": ('311311222', ["Ho", "Pm"]),
    "Tm": ('11131221133112', ["Er", "Ca", "Co"]),
    "Yb": ('1321131112', ["Tm"]),
    "Lu": ('311312', ["Yb"]),
    "Hf": ('11132', ["Lu"]),
    "Ta": ('13112221133211322112211213322113', ["Hf", "Pa", "H", "Ca", "W"]),
    "W": ('312211322212221121123222113', ["Ta"]),
    "Re": ('111312211312113221133211322112211213322113', ["Ge", "Ca", "W"]),
    "Os": ('1321132122211322212221121123222113', ["Re"]),
    "Ir": ('3113112211322112211213322113', ["Os"]),
    "Pt": ('111312212221121123222113', ["Ir"]),
    "Au": ('132112211213322113', ["Pt"]),
    "Hg": ('31121123222113', ["Au"]),
    "Tl": ('111213322113', ["Hg"]),
    "Pb": ('123222113', ["Tl"]),
    "Bi": ('3113322113', ["Pm", "Pb"]),
    "Po": ('1113222113', ["Bi"]),
    "At": ('1322113', ["Po"]),
    "Rn": ('311311222113', ["Ho", "At"]),
    "Fr": ('1113122113', ["Rn"]),
    "Ra": ('132113', ["Fr"]),
    "Ac": ('3113', ["Ra"]),
    "Th": ('1113', ["Ac"]),
    "Pa": ('13', ["Th"]),
    "U": ('3', ["Pa"]),
    "Np": ('1311222113321132211221121332211N', ["Hf", "Pa", "H", "Ca", "Pu"]),
    "Pu": ('31221132221222112112322211N', ["Np"]),
}

def _reverse_cosmology():
    reverse = {}
    for element, (string, _) in COSMOLOGY.items():
        reverse[element] = (string, [])
    for parent, (string, children) in COSMOLOGY.items():
        for child in children:
            reverse[child][1].append(parent)
    return reverse

REVERSE_COSMOLOGY = _reverse_cosmology()
ELEMENTS = {_str: name for name, (_str, _) in COSMOLOGY.items()}

def split_to_elements(string: str) -> List[Tuple[str, int]]:

    # Special case for day 0
    if string in ELEMENTS:
        return [(ELEMENTS[string], 0)]
    # Special case for day 1
    string = lns(string)
    if string in ELEMENTS:
        return [(ELEMENTS[string], 1)]

    def _rec_split(_string, depth):
        if _string in ELEMENTS:
            yield (ELEMENTS[_string], depth)
            return
        for atom in memoized_split_lns(_string):
            yield from _rec_split(atom, depth+1)

    # Day 2 onwards: replace >=4 digits by N, this allows us
    # to manipulate 2 transuranic elements instead of 12.
    string = re.sub('[4-9]', 'N', lns(string))
    return list(_rec_split(string, 2))

def make_length_iterators(names: List[str]) -> Dict[str, List[Iterator[int]]]:

    class RootIterator:
        def __init__(self, string):
            self.string = string
            self.sub_iters = []
            self._start = True

        def __iter__(self):
            return self

        def __next__(self):
            if self._start:
                self._start = False
                return len(self.string)
            return sum(next(i) for i in self.sub_iters)

    counts = Counter(names)
    roots, subs, views = {}, {}, {}

    for name, (_str, parents) in REVERSE_COSMOLOGY.items():
        n = len(parents)
        roots[name] = RootIterator(_str)
        sub_iters = tee(roots[name], n + counts[name])
        subs[name] = list(sub_iters[:n])
        if name in counts:
            views[name] = list(sub_iters[n:])

    for name, (_, children) in COSMOLOGY.items():
        for child in children:
            roots[name].sub_iters.append(subs[child].pop())

    assert all(not l for l in subs.values())
    return views
