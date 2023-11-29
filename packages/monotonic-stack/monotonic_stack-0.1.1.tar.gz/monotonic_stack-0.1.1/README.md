# Monotonic Stack

The monotonic increasing stack and monotonic decreasing stack, namely monotonic stack, is a very powerful tool for finding next greater/smaller element.
More specifically, always **use monotonic increasing stack when we are trying to find the next smaller element, vice versa.**
The typical usage of monotonic stack is to find the next greater/smaller element in an array.

```
pip install monotonic_stack
```


This monotonic stack:
- works with any Python sequence, not just strings, if the items are hashable
- is implemented in pure Python

PyPi: https://pypi.org/project/monotonic-stack/

## Usage

``` py
>>> from monotonic_stack import MonotonicStack
>>> MS = MonotonicStack([1, 2, 3, 4, 5])
>>> MS.next_greater_on_right()
[2, 3, 4, 5, -1]
>>> MS.next_greater_on_left()
[-1, 1, 2, 3, 4]
>>> MS.next_smaller_on_right()
[-1, -1, -1, -1, -1]
>>> MS.next_smaller_on_left()
[-1, -1, -1, -1, -1]
```
