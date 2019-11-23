from itertools import groupby
import re

# "manual" computation of Look and Say, with a for loop
def imperative_look_and_say(string: str):
    """'Direct' implementation of the Look-and-Say logic"""
    result, times, repeat = '', 1, string[0]
    for char in string[1:]:
        if char != repeat:
            result += str(times) + repeat
            times, repeat = 1, char
        else:
            times += 1
    result += str(times) + repeat
    return result

# RegEx computation of Look and Say
RE_LNS = re.compile(r'((.)\2*)')

def regex_look_and_say(string: str):
    """RegEx-based Look-and-Say logic"""
    return ''.join(
        str(len(g)) + g[0]
        for g, _ in RE_LNS.findall(string)
    )

# Itertools-based approach
def groupby_look_and_say(string: str):
    """itertools-based Look-and-Say logic"""
    return ''.join(
        str(len(list(g))) + k
        for k, g in groupby(string)
    )

look_and_say = imperative_look_and_say

def brute_deep_lns(string: str, depth: int, call=look_and_say):
    """
    Simple Look-and-Say calculation at depth, by calling the base
    logic as many times as needed. Quite slow.
    """
    for _ in range(depth):
        string = call(string)
    return string
