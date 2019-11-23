from hypothesis import given, strategies as st
import pytest

from look_and_say import compute_length as lengths
from look_and_say.compute_deep import list_deep_lns
from look_and_say.testing import lns_nice_strings

FUNCTIONS = [
    lengths.recursive_lns_length,
    lengths.cached_lns_length,
    lengths.stack_lns_length,
    lengths.parallel_lns_length,
    lengths.cosmology_lns_length,
]

depths = st.integers(min_value=0, max_value=40)


@given(string=lns_nice_strings, depth=depths)
@pytest.mark.parametrize("call", FUNCTIONS)
def test_fast_length(call, string, depth):
    expected = sum(map(len, list_deep_lns(string, depth)))
    assert call(string, depth) == expected
