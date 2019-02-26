"""
Simple file combining the examples in the presentation,
to demonstrate the pytest integration.
"""

import re
from hypothesis import given, strategies, assume


def extract_id(str_id: str) -> int:
    if str_id[0] == 'c' and str_id[1:].isdigit():
        return int(str_id[1:])
    return -1


# Tests

RE_NUMBER = re.compile(r'^[0-9]+$')

@given(strategies.integers(min_value=0))
def test_int_always_decodes(number):
    assert extract_id(f'c{number}') == number

    
@given(strategies.characters(), strategies.integers(min_value=0))
def test_not_c_never_decodes(char, number):
    assume(char != 'c')
    assert extract_id(f'{char}{number}') == -1


@given(strategies.text())
def test_never_crashes(any_string):
    assert isinstance(extract_id(any_string), int)


@given(strategies.text())
def test_no_false_positives(not_a_number):
    assume(RE_NUMBER.match(not_a_number) is None)
    assert extract_id(f'c{not_a_number}') == -1
