import pytest

from look_and_say.core import split, look_and_say
from look_and_say.cosmology import COSMOLOGY, ELEMENTS


@pytest.mark.parametrize("element,entry", COSMOLOGY.items())
def test_cosmology_validity(element, entry):
    string, products = entry
    children = split(look_and_say(string))
    assert products == [ELEMENTS[c] for c in children]
