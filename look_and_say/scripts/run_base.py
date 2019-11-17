from look_and_say.base import (
    brute_deep_lns,
    groupby_look_and_say,
    imperative_look_and_say,
    regex_look_and_say,
)

res = brute_deep_lns('1', 40, regex_look_and_say)
print(len(res))
