---?color=linear-gradient(45deg, white 80%, #ffde57 80%, #ffde57 87%, #4584b6 87%)

# What's New In Python 3.8?

Xavier Villaneau

---?color=linear-gradient(0deg, white 70%, #ffde57 70%, #ffde57 76%, #4584b6 76%)

@snap[north span-100 h2-white]
## Python 3 Feelings over time
@snapend

@snap[west span-30 text-center text-15 fragment]
2016  
¯\\\_(ツ)\_/¯
@snapend

@snap[midpoint span-30 text-center text-15 fragment]
2017  
🤔
@snapend

@snap[east span-30 text-center text-15 fragment]
2018  
🥰
@snapend

---?color=linear-gradient(90deg, #4584b6 7%, #ffde57 7%, #ffde57 10%, white 10%)

## What's New In Python 3.8?

Python 3.8.0b1, July 4, 2019:  
@css[text-black](https://docs.python.org/3.8/whatsnew/3.8.html)

---?image=python38/assets/img/walrus.jpg&size=cover

@snap[south-east span-50 text-07 text-right]
Copyright © 2015 Gary Bembridge
@snapend

---?color=linear-gradient(90deg, #4584b6 7%, #ffde57 7%, #ffde57 10%, white 10%)

### Assignment

Normally:
```py
>>> x = 1
>>> y = (z = 2)
  File "<stdin>", line 1
    y = (z = 2)
           ^
SyntaxError: invalid syntax
```

+++?color=linear-gradient(90deg, #4584b6 7%, #ffde57 7%, #ffde57 10%, white 10%)

### Assignment Expressions

New in 3.8:
```py
>>> y = (z := 2)
>>> y, z
(2, 2)

```

---?color=linear-gradient(90deg, #4584b6 7%, #ffde57 7%, #ffde57 10%, white 10%)

### Examples

Handle a matched regex
```py
if (match := pattern.search(data)) is not None:
    # Do something with match
```

Loop over things
```py
while chunk := file.read(8192):
   process(chunk)
```

+++?color=linear-gradient(90deg, #4584b6 7%, #ffde57 7%, #ffde57 10%, white 10%)

### More Examples

Reuse a value that's expensive to compute
```py
[y := f(x), y**2, y**3]
```

Share a value in a comprehension
```py
filtered_data = [y for x in data if (y := f(x)) is not None]
```

---?color=linear-gradient(90deg, #4584b6 7%, #ffde57 7%, #ffde57 10%, white 10%)

### The Story of PEP 572

![](python38/assets/img/pep-572.png)

---?image=python38/assets/img/avay.jpg&size=cover

---?color=linear-gradient(92deg, #4584b6 6%, #ffde57 8%, white 10%)

### Once the dust settles…

![](python38/assets/img/gvr_resigns.png)

---?color=linear-gradient(90deg, #4584b6 7%, #ffde57 7%, #ffde57 10%, white 10%)

### Leadership Follow-Up

@ul
- PEP 8001 — Python Governance Voting Process
- PEP 8016 — The Steering Council Model
- PEP 8100 — January 2019 steering council election
- PEP 572 — Assignment Expressions
@ulend

---?color=linear-gradient(90deg, #4584b6 7%, #ffde57 7%, #ffde57 10%, white 10%)

## Positional-Only Arguments

@[1-3]
@[4-7]
@[8-11]
@[12-15]
```py
>>> def f(x, /, y, *, z):
...     print(x, y, z)
... 
>>> f(1, 2, z=3)
1 2 3
>>> f(1, y=2, z=3)
1 2 3
>>> f(1, 2, 3)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: f() takes 2 positional arguments but 3 were given
>>> f(x=1, y=2, z=3)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: f() got some positional-only arguments passed as keyword arguments: 'x'
```

---?color=linear-gradient(90deg, #4584b6 7%, #ffde57 7%, #ffde57 10%, white 10%)

## f-string debugging with =

```py
>>> x = 71
>>> f'Looks like {x=} and {x*3-1=}'
'Looks like x=71 and x*3-1=212'
```

---?color=linear-gradient(90deg, #4584b6 7%, #ffde57 7%, #ffde57 10%, white 10%)

## Other
@ul
- Added `math.dist()` for computing Euclidean distance between two points
- Added `math.prod()` analogous to `sum()` for products
- New `shlex.join()` acts as the inverse of `shlex.split()`
- `SyntaxWarning` when `is` or `is not` are used with strings or ints
@ulend

---?color=linear-gradient(90deg, #4584b6 7%, #ffde57 7%, #ffde57 10%, white 10%)

## What is new in Python 3.9?

@ul
- PEP 554 — Multiple Interpreters in the Stdlib
- PEP 594 — Removing dead batteries from the standard library (¯―¯٥)
@ulend

---?color=linear-gradient(45deg, white 80%, #ffde57 80%, #ffde57 87%, #4584b6 87%)

# Thank you!

Xavier Villaneau  

@size[0.8em](xvillaneau@gmail.com | blog.villaneau.fr | @xvillaneau)
