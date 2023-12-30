from ast import Tuple
import time
from typing import Dict
from MelodieFuncFlow import (
    MelodieGenerator,
    MelodieFrozenGenerator,
    compose,
    melodie_generator,
)


def test_generator():
    out = []
    for item in MelodieGenerator([1, 2, 3]):
        out.append(item)
    assert out == [1, 2, 3]


def test_head():
    g = MelodieGenerator([1, 2, 3]).f
    assert g.head() == 1
    assert g.head() == 1
    assert g.head() == 1
    g = MelodieGenerator([1, 2, 3])

    assert g.head() == 1
    assert g.head() == 2
    assert g.head() == 3


def test_attributes():
    assert MelodieGenerator([1 + 1j, 1 + 2j, 3 + 5j]).attributes("imag").l == [1, 2, 5]


def test_cast():
    assert MelodieGenerator([1, 2, 3, 4, 5]).map(lambda x: float(x)).cast(float).l


def test_iteration_on_generator():
    g = MelodieGenerator(iter([1, 2, 3, 4, 5]))

    for item in g:
        pass
    remaining = []
    for item in g:
        remaining.append(item)
    assert len(remaining) == 0


def test_filter():
    assert MelodieGenerator([1, 2, 3, 4, 5]).filter(lambda x: x > 3).l == [4, 5]


def test_slice():
    assert [2, 3] == MelodieGenerator(iter([1, 2, 3, 4, 5])).slice(1, 3).to_list()
    assert [1, 2, 3] == MelodieGenerator(iter([1, 2, 3, 4, 5])).slice(0, 3).to_list()

    # g = MelodieGenerator(range(5))
    assert [0, 1, 2] == MelodieGenerator(range(5)).slice(0, 3).to_list()
    assert [0, 1, 2] == MelodieGenerator(range(5))[0:3].to_list()
    # g = MelodieGenerator(range(5))
    assert [0, 1] == MelodieGenerator(range(5))[:2].to_list()
    assert [0, 1] == MelodieGenerator(range(5)).slice(2).to_list()

    assert MelodieGenerator(range(5)).slice(2, -1).to_list() == [2, 3, 4]
    assert MelodieGenerator(range(5))[2:].to_list() == [2, 3, 4]

    try:
        MelodieGenerator([1, 2, 3])[0:3:2]
        raise ValueError
    except NotImplementedError:
        pass
    
    # test getting single element
    assert 3 == MelodieGenerator(range(5))[3]
    assert 3 == MelodieGenerator(range(5)).f[3]


def test_reduce():
    g = MelodieGenerator(iter([1, 2, 3, 4, 5])).freeze()
    ret = g.reduce(lambda sum, b: sum + b, 0)
    assert ret == 15
    ret = g.slice(2).reduce(lambda sum, b: sum + b, 0)
    assert ret == 3

    assert MelodieGenerator(iter([1, 2, 3, 4, 5])).reduce(lambda a, b: a + b) == 15


def test_folding_left():
    def add_to_dict(d: Dict, val):
        d[val] = val
        return d

    ret = MelodieGenerator(iter([1, 2, 3, 4, 5])).fold_left(add_to_dict, {})
    for i in [1, 2, 3, 4, 5]:
        assert ret[i] == i

    def add_to_dict_2(dic, elem):
        k, v = elem
        dic[k] = v
        return dic

    ret = MelodieGenerator([("Alice", 98), ("Bob", 76)]).fold_left(add_to_dict_2, {})
    assert {"Alice": 98, "Bob": 76} == ret


def test_iteration_on_frozen():
    g = MelodieFrozenGenerator([1, 4, 3, 2, 5])
    for item in g:
        pass
    g1 = g.sort(lambda x: x, reverse=True)
    assert g1.to_list() == [5, 4, 3, 2, 1]
    assert g.to_list() == [1, 4, 3, 2, 5]

    # if reverse==False and hope to get ascending data:
    #   left >  right, return 1
    #   left <  right, return -1
    #   left == right, return 0
    g2 = g.relsort(lambda x, y: 1 if x > y else 0 if x == y else -1)
    assert g2.to_list() == [1, 2, 3, 4, 5]
    remaining = []
    for item in g:
        remaining.append(item)
    assert len(remaining) == 5


def test_freeze():
    g = MelodieGenerator([1, 2, 3, 4, 5]).freeze()
    assert len(g) == 5
    assert g.len == 5

    for item in g:
        pass
    remaining = []
    for item in g:
        remaining.append(item)
    assert len(remaining) == 5
    try:
        next(g)
        raise ValueError("Must raise an error above")
    except NotImplementedError:
        pass


def test_star():
    assert [0, 2, 4, 6, 8] == MelodieGenerator(((i, i) for i in range(5))).star_map(
        lambda x, y: x + y
    ).to_list()

    assert [(1, 1), (3, 3), (5, 5), (7, 7), (9, 9)] == MelodieGenerator(
        ((i, i) for i in range(10))
    ).star_filter(lambda x, y: x % 2 == 1).to_list()


def test_indexed():
    ret = (
        MelodieGenerator([1, 3, 4, 2, 1])
        .indexed_filter(lambda i, val: val % 2 == 0 and i % 2 == 0)
        .to_list()
    )
    assert ret == [4]

    assert [0, 4, 6, 6] == MelodieGenerator([0, 4, 3, 2]).indexed_map(
        lambda i, val: i * val
    ).l


def test_indexed_extra_job():
    l = []

    def job(index, x):
        l.append(index)

    MelodieGenerator([1, 2, 3, 4, 5]).indexed_extra_job(job).exhaust()
    assert l == [0, 1, 2, 3, 4]


def test_process():
    g = MelodieGenerator([1, 2, 3, 4, 5]).freeze()
    g.show_progress().extra_job(lambda x: time.sleep(0.1)).to_list()

    g = MelodieGenerator([1, 2, 3, 4, 5])
    g.show_progress().extra_job(lambda x: time.sleep(0.1)).to_list()


def test_conv():
    assert MelodieGenerator([1, 2, 3, 3, 4]).to_set() == {1, 2, 3, 4}
    assert MelodieGenerator([1, 2, 3, 3, 4]).s == {1, 2, 3, 4}


def test_decorators():
    @melodie_generator
    def f():
        for i in range(3):
            yield i

    assert f().to_list() == [0, 1, 2]
