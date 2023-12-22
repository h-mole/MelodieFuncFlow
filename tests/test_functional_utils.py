from typing import Tuple
from MelodieFuncFlow import compose


def add(a, b) -> int:
    return a + b


def multiply_2(a, b) -> int:
    return a * 2, b * 2


def func(a, b) -> Tuple[int, int]:
    return a, b


def test_functional_operators():
    composed = compose(add, multiply_2, func)
    assert composed(1, 2) == 6
