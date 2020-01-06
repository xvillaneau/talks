from functools import wraps

from . import core, compute_deep as deep, compute_length as length

AOC_EXAMPLE = "1113122113"

LNS_CALLS = {
    "imperative": core.imperative_look_and_say,
    "regex": core.regex_look_and_say,
    "groupby": core.groupby_look_and_say,
}


def make_lns_test(method, depth, string="1"):
    call = LNS_CALLS[method]

    def inner():
        return deep.brute_deep_lns(string, depth, call)

    return inner


DEEP_CALLS = {
    "brute": deep.brute_deep_lns,
    "list": deep.list_deep_lns,
    "linked": deep.linked_deep_lns,
    "recursive": deep.recursive_deep_lns,
    "stack": deep.stack_deep_lns,
}


def make_deep_test(method, depth, string="1"):
    call = DEEP_CALLS[method]

    def inner():
        return "".join(call(string, depth))

    return inner


def _len_from_atoms(func):
    @wraps(func)
    def inner(*args, **kwargs):
        return sum(map(len, func(*args, **kwargs)))

    return inner


LENGTH_CALLS = {
    "list": _len_from_atoms(deep.list_deep_lns),
    "recursive": length.recursive_lns_length,
    "parallel": length.parallel_lns_length,
    "cosmology": length.cosmology_lns_length,
}


def make_length_test(method, depth, string="1"):
    call = LENGTH_CALLS[method]

    def inner():
        if hasattr(call, "cache_clear"):
            call.cache_clear()
        core.memoized_step.cache_clear()
        try:
            return call(string, depth)
        except RecursionError:
            raise SystemExit(0) from None

    return inner
