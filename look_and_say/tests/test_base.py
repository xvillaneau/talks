import pytest

from look_and_say import base as lns

EXPECTED_RESULTS = [
    ('1', '11'),
    ('11', '21'),
    ('21', '1211'),
    ('1211', '111221'),
    ('111221', '312211'),
    ('312211', '13112221'),
    ('41111', '1441'),
    ('1441', '112411'),
    ('11131221131211', '311311222113111221'),
]

FUNCTIONS = [
    lns.imperative_look_and_say,
    lns.regex_look_and_say,
    lns.groupby_look_and_say,
]

@pytest.mark.parametrize('string,description', EXPECTED_RESULTS)
@pytest.mark.parametrize('call', FUNCTIONS)
def test_look_and_say_base(string, description, call):
    assert call(string) == description