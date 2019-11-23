from hypothesis import given, strategies as st
import pytest

from look_and_say import compute_deep
from look_and_say.testing import lns_nice_strings, lns_strings

FUNCTIONS = [
    compute_deep.list_deep_lns,
    compute_deep.linked_deep_lns,
    compute_deep.recursive_deep_lns,
    compute_deep.stack_deep_lns,
]

depths = st.integers(min_value=0, max_value=10)


@given(string=lns_nice_strings, depth=depths)
@pytest.mark.parametrize("call", FUNCTIONS)
def test_deep_lns_nice_strings(call, string, depth):
    expected = compute_deep.brute_deep_lns(string, depth)
    assert "".join(call(string, depth)) == expected


@given(string=lns_strings, depth=depths)
@pytest.mark.parametrize("call", FUNCTIONS)
def test_deep_lns_tricky_strings(call, string, depth):
    expected = compute_deep.brute_deep_lns(string, depth)
    assert "".join(call(string, depth)) == expected
