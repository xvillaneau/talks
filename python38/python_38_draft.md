# What's New in Python 3.8?

## Assignment Expressions

https://www.python.org/dev/peps/pep-0572/
https://mail.python.org/pipermail/python-dev/2018-July/154601.html
https://mail.python.org/pipermail/python-committers/2018-July/005664.html
https://www.python.org/dev/peps/pep-8016/

## Positional-only parameters

https://www.python.org/dev/peps/pep-0570/

## Parallel filesystem cache for compiled bytecode files

New env var, PYTHONPYCACHEPREFIX

## f-strings now support = for quick and easy debugging

## Other

- functools.lru_cache() can now be used as a straight decorator
- Added new function math.dist() for computing Euclidean distance between two points
- Added new function, math.prod(), as analogous function to sum()
- The new shlex.join() function acts as the inverse of shlex.split()
- The compiler now produces a SyntaxWarning when identity checks (is and is not) are used with certain types of literals (e.g. strings, ints)
