# MelodieFunctFlow

[![Tests](https://github.com/hzyrc6011/MelodieFuncFlow/actions/workflows/python-app.yml/badge.svg)](https://github.com/hzyrc6011/MelodieFuncFlow/actions/workflows/python-app.yml)

## Description

Functional programming extension of Melodie. Using this tool, you can make
 full use of the advantages of functional programming, making coding more
 convenient and debugging easier.

## Getting Started

### Dependencies

- Python 3.8+
- No compulsory dependency. But to use `show_progress` to show the progress,
    `tqdm` is required.

### Installing

```bash
pip install MelodieFuncFlow
```

## Basic Tutorial

To take advantage of functional programming in
 interactive mode, we strongly suggest to use
 `IPython`/`Jupyter` instead of barely `Python`.

Also, for script-based programming, MelodieFuncFlow
 has optimized type hints for the autocompletion
 of many common editors. But for convenience, this
 documentation only used interactive environment for
 demonstration.

### Creating Generator

The core class is `MelodieGenerator`.
 By the code below, we imported `MelodieGenerator`,
 and created one instance `g`.

```python
In [1]: from MelodieFuncFlow import MelodieGenerator

In [2]: g = MelodieGenerator([1, 2, 3, 4, 5])
```

### Iterate Through The MelodieGenerator

This generator is also an `Iterable`:

```python
In [3]: [item for item in MelodieGenerator([1, 2, 3, 4, 5])]
Out[3]: [1, 2, 3, 4, 5]
```

### Basic Conversions

MelodieGenerator could be converted to `list` or `set`.

- `to_list` put elements to a new list in the order the
 `MelodieGenerator` generates
- `to_set` will put elements to a set, eliminating
 repetitions of elements.

```python
In [4]: MelodieGenerator([1, 2, 3, 1, 2]).to_list()
Out[4]: [1, 2, 3, 1, 2]

In [5]: MelodieGenerator([1, 2, 3, 1, 2]).to_set()
Out[5]: {1, 2, 3}
```

Of course, if some elements in generator are not
 hash-able, `to_set` method will raise an `TypeError`:

```python
In [6]: MelodieGenerator([{"a": 123}, {"a": 456}, {"a": 123}]).to_set()

↓↓↓↓↓↓ raised an error ↓↓↓↓↓↓

TypeError: unhashable type: 'dict'
```

### Accessing the Elements of the Generator

We can access the first element by `head`:

```python
In [2]: g = MelodieGenerator([1, 2, 3, 4, 5])

In [3]: g.head()
Out[3]: 1

In [4]: g.head()
Out[4]: 2

In [5]: g.head()
Out[5]: 3
```

Also, we can `slice` this generator. The two arguments of
this method are lower bound (required) and upper bound (`-1` by
default), left-close and right-open.
 If the upper bound is less than zero, it will be regarded as
 infinite:

```python
In [2]: MelodieGenerator([1, 2, 3, 4, 5]).slice(1, 3).to_list()
Out[2]: [2, 3]

In [3]: MelodieGenerator([1, 2, 3, 4, 5]).slice(1, -1).to_list()
Out[3]: [2, 3, 4, 5]

In [4]: MelodieGenerator([1, 2, 3, 4, 5]).slice(2).to_list()
Out[4]: [3, 4, 5]
```

### Mapping

This generator supports mapping,
 which is a common method used in functional
 programming.

Mapping on the `MelodieGenerator` will not change
the original generator, but create a new
generator containing the return values
of the operator function in order.

```python
In [7]:  MelodieGenerator([1, 2, 3, 4, 5]).map(lambda x: x * x)
Out[7]: <MelodieFuncFlow.functional.MelodieGenerator at 0x28a5a641640>

In [8]: MelodieGenerator([1, 2, 3, 4, 5]).map(lambda x: x * x).to_list()
Out[8]: [1, 4, 9, 16, 25]
```

> Note: The `to_list` method called above is
 intended to let the generator go on. As the values
 in the `MelodieGenerator` is evaluated lazily,
 only calling `map` method will just create a new
 generator, which will not execute automatically
 (demonstrated in `Out[7]`).

If the elements inside `MelodieGenerator` are `tuple`s
of same size, `star_map` method can be used for better
organizing the operator function. Here is a demo
to convert students' grades from 100 to 5:

```python
In [9]: MelodieGenerator([("Alice", 98), 
                           ("Bob", 95), 
                           ("Carol", 92)]) \
                .star_map(lambda name, grade: grade*5/100) \
                .to_list()
Out[9]: [4.9, 4.75, 4.6]
```

Code `In [9]` has the same effect of the code below.
As we can see, coding with `star_map` is easier for
understanding the operator.

```python
MelodieGenerator([("Alice", 98), 
                           ("Bob", 95), 
                           ("Carol", 92)]) \
                .map(lambda student: student[1]*5/100) \
                .to_list()
```

### Filtering

Filtering is another common operation in functional
programming. The `filter` method is used to
extract elements from the iterator that meet
specific conditions.
The `filter` method does not change the original
generator, but returns a new generator with all
the elements that satisfy the condition.

```python
In [10]: MelodieGenerator([1, 2, 3, 4, 5]).filter(lambda x: x % 2 == 0).to_list()
Out[10]: [2, 4]
```

Also, `MelodieGenerator` supports `star_filter`, unpacking
the tupled elements to match the arguments of condition function.

```python
In [11]: MelodieGenerator([(1, 0), (0, -5), (0, -3)]).star_filter(lambda x, y: y < 0).to_list()
Out[11]: [(0, -5), (0, -3)]
```

### Reducing

#### Brief Introduction to Reducing

In functional programming, reducing refers to the process
of applying a binary operator function (a function that takes
two arguments) to all elements of an iterable
(such as a list or array), in a cumulative way,
so as to reduce the iterable to a single output value.

The binary function is applied to the first two elements
of the iterable, then to the result and the next element,
 and so on, until only one element remains.
This final element is the output value of the reduction.

Here is an example written with standard libraries.
suppose we have a list of numbers and we want to find
 their product.
 the `reduce`
is performed on the list `numbers`.

```python
from functools import reduce

numbers = [1, 2, 3, 4, 5]
product = reduce((lambda x, y: x * y), numbers)
print(product)  # Output: 120
```

The calculation steps are listed below. (
`lambda x, y: x * y` is written as `product(x, y)`):

1. product(1, 2) = **2**,     remaining values were [3, 4, 5]
2. product(**2**, 3) = **6**, remaining values were [4, 5]
3. product(**6**, 4) = **24**, remaining values were [5]
4. product(**24**, 5) = **120**, remaining values were []

So finally we got the value **120**.

#### Example for MelodieGenerator

An reducing example for MelodieGenerator is as follows.
Note that initial value is required now.

```python
>>> MelodieGenerator([-1, 1, 3, 5]).reduce(lambda x, y: x + y, 0)
8

>>> MelodieGenerator([[-1], [1, 3, 5]]).reduce(lambda x, y: x + y, []) 
[-1, 1, 3, 5]

def add_to_dict(dic, elem):
    k, v = elem
    dic[k] = v
    return dic

>>> MelodieGenerator([("Alice", 98), ("Bob", 76)]).reduce(add_to_dict, {})         
{'Alice': 98, 'Bob': 76}
```

### Extra Jobs

Extra jobs by `extra_job` in `MelodieGenerator` is a kind of
operation that will not interfere the computation flow.

For example, in code `In [13]` and `In [14]`, a `print`
is inserted into the computation flow in two different
positions, and middle results
were printed.
However, the result `Out[13]` and `Out[14]` are also the
same as the original result `Out[12]`:

```python
In [12]: MelodieGenerator([-1, 1, 3, 5]).map(lambda value: value * 2).to_list()
Out[12]: [-2, 2, 6, 10]

In [13]: MelodieGenerator([-1, 1, 3, 5]).extra_job(print).map(lambda value: value * 2).to_list()
-1
1
3
5
Out[13]: [-2, 2, 6, 10]

In [14]: MelodieGenerator([-1, 1, 3, 5]).map(lambda value: value * 2).extra_job(print).to_list()
-2
2
6
10
Out[14]: [-2, 2, 6, 10]
```

### Indexed Filtering, Mapping and Extra Job

Sometimes it is important for the mapping/filtering/extra-job operator
to get the index of current element.
To do this, we implemented `indexed_filter`, `indexed_map` and `indexed_extra_job`,
providing an index together with each element.

```python
In [15]: MelodieGenerator([-1, 1, 3, 5]).indexed_map(lambda index, value: (index, value)).to_list()
Out[15]: [(0, -1), (1, 1), (2, 3), (3, 5)]

In [16]: MelodieGenerator([1, 2, 3, 4]).indexed_filter(lambda index, value: index > 1 and value % 2 == 0).to_list()
Out[16]: [4]

In [17]: MelodieGenerator([-1, 1, 3, 5]).indexed_extra_job(print).to_list()
0 -1
1 1
2 3
3 5
Out[17]: [-1, 1, 3, 5]
```

> Note: Currently, indexed map/filter with tuple unpacks have
not been implemented.

### Freeze the Generator

You might have noticed that in the examples above,
`MelodieGenerator` was evaluated right after the creation.
That is because this generator is irreversible, we cannot
evaluate it for the second time
(e.g., by `head`, `to_list`, `to_set` or `slice`) :

```python
>>> g =  MelodieGenerator([-1, 1, 3, 5])
>>> g.to_list()
[-1, 1, 3, 5]
>>> g.to_list()
[]
```

If you want to evaluate it repeatedly, you could `freeze` it.
`freeze` will generate a `MelodieFrozenGenerator` object,
which is a subclass of `MelodieGenerator`.

Most of the method implementations in `MelodieFrozenGenerator`
are identical to `MelodieGenerator`, and it can be evaluated
multiple times.

```python
>>> g = MelodieGenerator([-1, 1, 3, 5]).freeze()
>>> g.to_list()
[-1, 1, 3, 5]
>>> g.to_list()
[-1, 1, 3, 5]
```

#### Sorting the Frozen Generator

Besides, frozen generator can be sorted.
Method `sort` will return a new
`MelodieFrozenGenerator` with elements sorted.

```python
>>> g = MelodieGenerator([1, 3, 4, 2, 5]).freeze()
>>> g.sort(lambda x: x).to_list() # ascending by default
[1, 2, 3, 4, 5]
>>> g.sort(lambda x: x, reverse=True).to_list() # descending 
[5, 4, 3, 2, 1]
```

To sort by a custom comparator function:

```python
def cmp(a, b):
    if a == b:
        return 0
    elif a > b:
        return 1
    else:   
        return -1

>>> g = MelodieGenerator([1, 3, 4, 2, 5]).freeze()
>>> g.relsort(cmp).to_list() # ascending by default
[1, 2, 3, 4, 5]
>>> g.relsort(cmp, reverse=True).to_list() # descending
[5, 4, 3, 2, 1]
```

#### Differences between MelodieFrozenGenerator and MelodieGenerator

> Note 1: `head` method on frozen generator will always
return the first value

```python
>>> g = MelodieGenerator([1,2,3,4,5]).freeze()
>>> g.head()
1
>>> g.head()
1
```

### Showing Progress

> Note: `tqdm` must be installed. If you are using `IPython`,
`ipywidgets` is required as well. Just execute:

```bash
pip install tqdm
pip install ipywidgets # Used when using IPython/Jupyter.
```

To show progress, just use `show_progress` method.

```python
In [19]: import time
In [20]: MelodieGenerator([-1, 1, 3, 5]).extra_job(lambda x: time.sleep(1)).show_progress().to_list()
4it [00:04,  1.01s/it]
Out[20]: [-1, 1, 3, 5]
```

For frozen generator, as the total value is known,
`show_progress` will show the progress bar.

```python
>>> MelodieGenerator([-1, 1, 3, 5]).freeze().show_progress().extra_job(lambda x: time.sleep(1)).to_list() 
100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████| 4/4 [00:04<00:00,  1.01s/it]
```

## Version History

- 0.1
  - Initial Release

## License

This project is licensed under the MIT License - See the LICENSE.md file for details
