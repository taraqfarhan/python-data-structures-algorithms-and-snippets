## Overview

Arrays can be of two types.

1. Static (We can't modify the array)
2. Dynamic (We can modify the array)

#### Static (`array.array`, `tuple`, `str`)

Python does not have a built-in static array type. We can use the built-in `array` module to create arrays with a fixed size and data type (homogeneous), which makes them behave more like static arrays in terms of memory efficiency and type enforcement, although their size is still technically modifiable. If the data type in an array is a character, then that array is known as a string. Python strings are immutable. Moreover Python offers `tuple` sequences which can also be considered as a static array as they are immutable, but a `tuple` can store any types of data (heterogeneous).

#### Dynamic Arrays (`List`)

On the other hand Python offers `list` sequences, which is mutable. And we can store any type of data (heterogeneous) in a python list.

## Time Complexity

1. Access/Reading an element by index `O(1)`
2. Insertion at the end (if space available) `O(1)`
3. Insertion at the beginning or middle `O(n)` (requires shifting elements)
4. Deletion at the end `O(1)` (if using a "soft delete" or tracking size)
5. Deletion at the beginning or middle `O(n)` (requires shifting elements)
6. Searching for a value (unsorted) `O(n)` (linear search)

## Code for `array.array`

```python
>>> from array import array # importing `array` class from the array module

# get an array object array(typecode, sequence)
# The type code 'i' means signed integer
# to see other typecodes, type `help array` in the repl
>>> values = array('i', (4,1,6,7,2))
>>> values[2] # indexing
6
>>> values[-1] # negative indexing
2
>>> values[3:5] # slicing
array('i', [7, 2])

>>> values.append(45) # technically not truly static (appending an elem)
>>> values
array('i', [4, 1, 6, 7, 2, 45])
>>> values.insert(1,100)  # inserting 100 at index 1
>>> values
array('i', [4, 100, 1, 6, 7, 2, 45])

>>> values.remove(4)   # remove the first occurrence of 4
>>> values
array('i', [100, 1, 6, 7, 2, 45])
>>> values.remove(2)
>>> values
array('i', [100, 1, 6, 7, 45])
>>> values.pop(0)   # popping the first element
100
>>> values
array('i', [1, 6, 45, 7])
>>> values.pop()  # pop the last element (by default)
7

>>> values.tolist()   # convert the array to a python list obj
[1, 6, 45]
```

## Code for `str`

## Code for `tuple`

## Code for `list`