---?color=linear-gradient(45deg, white 80%, #ffde57 80%, #ffde57 87%, #4584b6 87%)

# A Python 3.8 Quirk

Xavier Villaneau

---?color=linear-gradient(90deg, #4584b6 7%, #ffde57 7%, #ffde57 10%, white 10%)

## What's New In Python 3.8?

### Assignment Expressions

```py
>>> if (x := True):
...     print(x)
True
```

### f-string Debug format

```py
>>> x = 71
>>> f'Looks like {x=} and {x*3-1=}'
'Looks like x=71 and x*3-1=212'
```

---?color=linear-gradient(90deg, #4584b6 7%, #ffde57 7%, #ffde57 10%, white 10%)

## But also in f-strings

Formatting specifiers:
```py
>>> print(1/7)
0.14285714285714285
>>> f'{1/7:.4f}'
'0.1429'
```

So what happens if…?

---?color=linear-gradient(90deg, #4584b6 7%, #ffde57 7%, #ffde57 10%, white 10%)

## Fuuuuuuusiiioon!!!

Introducing the "Reverse Walrus" `=:`

```py
>>> f'{1/7=:.5f}'
'1/7=0.14286'
```

Not an operator but an unfortunate syntax quirk.

---?color=linear-gradient(90deg, #4584b6 7%, #ffde57 7%, #ffde57 10%, white 10%)

## But wait, there's more!

You can use both `:=` and `=:` at the same time!

Example by Raymond Hettinger on Twitter:
```py
>>> from math import radians, sin
>>> for angle in range(0, 360):
...     print(f'{angle=}\N{degree sign} '
...           f'{(theta:=radians(angle))=:.3f} '
...           f'{sin(theta)=:.3f}')
... 
angle=0° (theta:=radians(angle))=0.000 sin(theta)=0.000
angle=1° (theta:=radians(angle))=0.017 sin(theta)=0.017
angle=2° (theta:=radians(angle))=0.035 sin(theta)=0.035
angle=3° (theta:=radians(angle))=0.052 sin(theta)=0.052
…
```

---?color=linear-gradient(45deg, white 80%, #ffde57 80%, #ffde57 87%, #4584b6 87%)

# Thank you!

Xavier Villaneau

@size[0.8em](This talk: https://gitpitch.com/xvillaneau/talks?p=reverse_walrus_LT)

@size[0.8em](xvillaneau@gmail.com | blog.villaneau.fr | @xvillaneau)
