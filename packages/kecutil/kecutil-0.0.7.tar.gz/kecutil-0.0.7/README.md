## KEC ITP: Python Util Functions

### Functions

> kecutil.reduce(cb(cur, val), list, default)
>
> Reduce is used to *reduce* a list to one value.
> This is commonly useful when finding the longest string for example
>
> ```python
> from kecutil import reduce
>
>
> strings = ["ab", "acb", "abcdef", "abd"]
> longestString = reduce(lambda x, y: x if len(x) > len(y) else y, strings, "")
>
> print(longestString) # "abcdef"
> ```

> kecutil.clearConsole()
>
> Clears the console window

> kecutil.clamp(value: int,length=2)
>
> Clamps a float to have the same number of decimals as the length
> Returns a new float
>
> ```python
> from kecutil import clamp
>
>
> number = 100.12345
> clampedTwo = clamp(number)
> clampedThree = clamp(number, 3)
>
> print(clampedTwo) # 100.12
> print(clampedThree) # 100.123
> print(type(clampedTwo)) # <class 'float'>
> print(type(clampedThree)) # <class 'float'>
> ```