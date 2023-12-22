import time
from MelodieFuncFlow import MelodieGenerator, MelodieFrozenGenerator, compose


def test_generator():
    pass


def test_iteration_on_generator():
    g = MelodieGenerator(iter([1, 2, 3, 4, 5]))

    for item in g:
        pass
    remaining = []
    for item in g:
        remaining.append(item)
    assert len(remaining) == 0


def test_slice():
    print("x", MelodieGenerator(iter([1, 2, 3, 4, 5])).slice(1, 3).to_list())
    assert [2, 3] == MelodieGenerator(iter([1, 2, 3, 4, 5])).slice(1, 3).to_list()
    assert [1, 2, 3] == MelodieGenerator(iter([1, 2, 3, 4, 5])).slice(0, 3).to_list()

    g = MelodieGenerator(range(5))
    assert [0, 1, 2] == g.slice(0, 3).to_list()
    assert [3, 4] == g.slice(3).to_list()


def test_reduce():
    g = MelodieGenerator(iter([1, 2, 3, 4, 5])).freeze()
    ret = g.reduce(lambda sum, b: sum + b, 0)
    assert ret == 15
    ret = g.slice(2).reduce(lambda sum, b: sum + b, 0)
    assert ret == 12


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


def test_iteration_with_freeze():
    g = MelodieGenerator([1, 2, 3, 4, 5]).freeze()

    for item in g:
        pass
    remaining = []
    for item in g:
        remaining.append(item)
    assert len(remaining) == 5


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


def test_process():
    g = MelodieGenerator([1, 2, 3, 4, 5]).freeze()
    g.show_progress().extra_job(lambda x: time.sleep(0.2)).to_list()
