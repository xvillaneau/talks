from itertools import groupby
import re

__all__ = (
    'imperative_look_and_say',
    'regex_look_and_say',
    'groupby_look_and_say',
    'brute_deep_lns',
)

# "manual" computation of Look and Say, with a for loo[
def imperative_look_and_say(string: str):
    """'Direct' implementation of the Look-and-Say logic"""
    result, times = "", 1
    repeat, *tail = string + " "
    for char in tail:
        if char != repeat:
            result += str(times) + repeat
            times, repeat = 1, char
            continue
        times += 1
    return result

# RegEx computation of Look and Say
RE_LNS = re.compile(r'(.)\1*')

def _lns_replace(match):
    return str(len(match.group())) + match.groups()[0]

def regex_look_and_say(string: str):
    """RegEx-based Look-and-Say logic"""
    return RE_LNS.sub(_lns_replace, string)

# Itertools-based approach
def groupby_look_and_say(string: str):
    """itertools-based Look-and-Say logic"""
    return ''.join(
        str(len(list(g))) + k
        for k, g in groupby(string)
    )

def brute_deep_lns(string: str, depth: int, call=imperative_look_and_say):
    """
    Simple Look-and-Say calculation at depth, by calling the base
    logic as many times as needed. Quite slow.
    """
    for _ in range(depth):
        string = call(string)
    return string
