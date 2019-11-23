from functools import wraps
from itertools import tee, islice


def parallel_iterator(generator_func):
    roots = {}

    @wraps(generator_func)
    def inner(*args):
        if args not in roots:
            roots[args] = generator_func(*args)
        iterator, roots[args] = tee(roots[args], 2)
        return iterator

    inner.cache_clear = roots.clear
    return inner


def iter_goto(iterable, n):
    if n < 0:
        return None
    return next(islice(iterable, n, None))
