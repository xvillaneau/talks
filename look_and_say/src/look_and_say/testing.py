import re
from hypothesis import strategies as st

RE_TEN = re.compile(r"(.)\1{9}")
RE_FOUR = re.compile(r"(.)\1{3}")

lns_strings = st.text(min_size=1, alphabet="123456789").filter(
    lambda s: RE_TEN.search(s) is None
)

lns_nice_strings = st.text(min_size=1, alphabet="123").filter(
    lambda s: RE_FOUR.search(s) is None
)
