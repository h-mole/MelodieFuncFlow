import functools


from typing import (
    Any,
    Callable,
    Generator,
    Generic,
    Iterable,
    List,
    Optional,
    Set,
    Type,
    TypeVar,
    Union,
    Tuple,
)

try:
    from typing import ParamSpec, TypeVarTuple
except:
    ParamSpec = TypeVar
    TypeVarTuple = TypeVar

VARTYPE = TypeVar("VARTYPE")
VARTYPE2 = TypeVar("VARTYPE2")
VARTYPE3 = TypeVar("VARTYPE3")
P = ParamSpec("P")


def _in_jupyter() -> bool:
    try:
        from IPython import get_ipython
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True   # Jupyter notebook or qtconsole
        else:
            return False
    except:
        return False


def _import_tqdm_module():
    if _in_jupyter():
        from tqdm.notebook import tqdm
    else:
        from tqdm import tqdm
    return tqdm


class MelodieGenerator(Generic[VARTYPE]):
    """
    A generator supporting some common functional-programming operations
    """

    def __init__(self, inner: Union[Generator[VARTYPE, None, None], Iterable[VARTYPE]]):
        self.inner = iter(inner)

    def __iter__(self):
        return self

    def __next__(self) -> VARTYPE:
        return self.inner.__next__()

    def attributes(self, attr: str) -> "MelodieGenerator[Any]":
        """
        Get attribute from each elements, returning a new generator containing
        attribute values.
        """

        def _(orig_gen):
            item: VARTYPE
            for item in orig_gen:
                yield getattr(item, attr)

        return MelodieGenerator(_(self.inner))

    def cast(self, t_: Type[VARTYPE2]) -> "MelodieGenerator[VARTYPE2]":
        """
        Cast returning type for each element of this iterator.
        """

        def _(orig_gen: MelodieGenerator[VARTYPE]):
            yield from orig_gen

        return MelodieGenerator(_(self.inner))

    def filter(
        self, condition: Callable[[VARTYPE], bool]
    ) -> "MelodieGenerator[VARTYPE]":
        """
        Filter elements that function ``condition`` returns ``True``
        """

        def _(orig_gen):
            item: VARTYPE
            for item in orig_gen:
                if condition(item):
                    yield item

        return MelodieGenerator(_(self.inner))

    def indexed_filter(
        self, condition: Callable[[int, VARTYPE], bool]
    ) -> "MelodieGenerator[VARTYPE]":
        """
        Filter elements that function ``condition`` returns ``True`` with index
        """

        def _(orig_gen):
            item: VARTYPE
            for i, item in enumerate(orig_gen):
                if condition(i, item):
                    yield item

        return MelodieGenerator(_(self.inner))

    def star_filter(
        self, condition: Callable[..., bool]
    ) -> "MelodieGenerator[VARTYPE]":
        """
        Filter elements that function ``condition`` returns ``True``.
        Each element will be unpacked by ``*elem``
        """

        def _(orig_gen):
            item: VARTYPE
            for item in orig_gen:
                if condition(*item):
                    yield item

        return MelodieGenerator(_(self.inner))

    def extra_job(self, func: Callable[[VARTYPE], Any]) -> "MelodieGenerator[VARTYPE]":
        """
        Inserting function call ``func(elem)`` in the middle of the calculation process of a functional
            program, which does not affect the calculation process.

        For example, the result of ``g.execute(print).map(lambda item: item.value)``
            is the same as ``g.map(lambda item: item.value)``,
            but the former has extra printouts for each element.
        """

        def _(orig_gen):
            item: VARTYPE
            for item in orig_gen:
                func(item)
                yield item

        return MelodieGenerator(_(self.inner))

    def indexed_extra_job(
        self, func: Callable[[int, VARTYPE], Any]
    ) -> "MelodieGenerator[VARTYPE]":
        """
        Like ``extra_job``, but with index.
        """

        def _(orig_gen):
            item: VARTYPE
            for i, item in enumerate(orig_gen):
                func(i, item)
                yield item

        return MelodieGenerator(_(self.inner))

    def map(self, func: Callable[[VARTYPE], VARTYPE2]) -> "MelodieGenerator[VARTYPE2]":
        """
        Map function ``func`` to each element
        """

        def _(orig_gen):
            item: VARTYPE
            for item in orig_gen:
                yield func(item)

        return MelodieGenerator(_(self.inner))

    def indexed_map(
        self, func: Callable[[int, VARTYPE], VARTYPE2]
    ) -> "MelodieGenerator[VARTYPE2]":
        """
        Map function ``func`` to each element
        """

        def _(orig_gen):
            item: VARTYPE
            for i, item in enumerate(orig_gen):
                yield func(i, item)

        return MelodieGenerator(_(self.inner))

    def star_map(self, func: Callable[..., VARTYPE2]) -> "MelodieGenerator[VARTYPE2]":
        """
        Map function ``func`` to each element with unpacking them by ``*elem``.
        """

        def _(orig_gen):
            item: VARTYPE
            for item in orig_gen:
                yield func(*item)

        return MelodieGenerator(_(self.inner))

    def parallel_map(
        self, func: Callable[..., VARTYPE2], star=False, init_code=""
    ) -> "MelodieGenerator[VARTYPE2]":
        """
        Map with ``ipyparallel``.

        Members in this package will be automatically imported.

        To use members from other packages, please inject the initialization
        code by ``init_code`` parameter.

        :init_code: Code to be executed ``before`` parallel execution.
        """
        from ipyparallel import Client

        c = Client()
        dview = c[:]
        code = """
        def update_props_to_globals(module):
            for item in dir(module):
                if not item.startswith("__"):
                    globals()[item] = getattr(module, item)
            
        def p():
            import MelodieStaticAnalysis
            import MelodieStaticAnalysis.clang_utils
            update_props_to_globals(MelodieStaticAnalysis.clang_utils)
            update_props_to_globals(MelodieStaticAnalysis)
        p()
        """
        dview.execute(code)
        cores = len(c[:])

        def _(orig_gen_: MelodieGenerator):
            orig_gen = iter(orig_gen_)
            async_tasks = []
            for _ in range(cores):
                arg = next(orig_gen)
                async_tasks.append(dview.map_async(func, [arg]))
            while async_tasks:
                async_task = async_tasks[0]
                if async_task.ready():
                    async_tasks.remove(async_task)
                    try:
                        arg = next(orig_gen)
                        async_tasks.append(dview.map_async(func, [arg]))
                    except StopIteration:
                        pass
                    yield async_task.result()[0]

        return MelodieGenerator(_(self))

    def reduce(
        self, func: Callable[[VARTYPE2, VARTYPE], VARTYPE2], initial: VARTYPE2
    ) -> VARTYPE2:
        """
        Perform reduce on this generator.
        """
        value = initial
        for item in self.inner:
            value = func(value, item)
        return value

    def exhaust(self) -> None:
        """
        Go through this generator until it is exhausted, returning ``None``.
        """
        for _ in self.inner:
            pass
        return

    def slice(self, start: int, stop: int = -1) -> "MelodieGenerator[VARTYPE]":
        """
        Select an interval of elements inside this generator, returning a new Generator.

        Like many other similar operations, the interval is close-left and open-right: ``[start, stop)``
        """
        assert start >= 0
        if stop >= 0:
            assert start < stop, (start, stop)

        def _(orig_gen: Iterable[VARTYPE]):
            if stop < 0:
                for i, item in enumerate(orig_gen):
                    if i >= start:
                        yield item
                    else:
                        continue
            else:
                for i, item in enumerate(orig_gen):
                    if start <= i < stop:
                        yield item
                    elif i < start:
                        continue
                    else:
                        break

        return MelodieGenerator(_(self.inner))

    def to_list(self) -> List[VARTYPE]:
        """
        Convert this generator to list
        """
        return list(self.inner)

    def to_set(self) -> Set[VARTYPE]:
        """
        Convert this generator to set
        """
        return set(self.inner)

    def freeze(self) -> "MelodieFrozenGenerator[VARTYPE]":
        """
        Convert the current iterator to a ``MelodieFrozenGenerator``.
        """
        lst = self.to_list()
        return MelodieFrozenGenerator(lst)

    def show_progress(self) -> "MelodieGenerator[VARTYPE]":
        """
        Show the progress of this iterator, without interfering the computation flow.

        For ``MelodieGenerator``, as the total number is not determined, a counter-only
        tqdm progress indicator will be shown like ``20it [00:02,  9.01it/s]``
        """
        tqdm = _import_tqdm_module()

        def _(orig_gen):
            bar = tqdm()
            item: VARTYPE
            for item in orig_gen:
                bar.update()
                yield item

        return MelodieGenerator(_(self.inner))

    def head(self) -> VARTYPE:
        """
        Get the first element of this generator
        """
        head = next(self)
        return head

    @property
    def l(self) -> List[VARTYPE]:
        """
        Shortcut property for ``to_list()`` method
        """
        return self.to_list()

    @property
    def s(self) -> Set[VARTYPE]:
        """
        Shortcut property for ``to_set()`` method
        """
        return self.to_set()

    @property
    def f(self) -> "MelodieFrozenGenerator[VARTYPE]":
        """
        Shortcut property for ``freeze()`` method
        """
        return self.freeze()


class SeqIter:
    """
    The iterator to deal with for-loops in AgentList or other agent containers
    """

    def __init__(self, seq: List[Any]):
        self._seq = seq
        self._i = 0

    def __next__(self):
        if self._i >= len(self._seq):
            raise StopIteration
        next_item = self._seq[self._i]
        self._i += 1
        return next_item


class MelodieFrozenGenerator(MelodieGenerator, Generic[VARTYPE]):
    """
    ``MelodieFrozenGenerator`` is like ``MelodieGenerator``, but it will start from the same
    head object when applying ``iter(g)`` on it for multiple times.
    """

    def __init__(self, inner: List[VARTYPE]):
        assert isinstance(
            inner, (list, tuple)
        ), f"parameter inner should be list or tuple, but got {inner}"
        self.inner = inner

    def __len__(self):
        return len(self.inner)

    def __iter__(self):
        return SeqIter(self.inner)

    def __next__(self) -> Any:
        raise NotImplementedError
    
    def head(self) -> Any:
        return self.inner[0]

    def show_progress(self) -> MelodieGenerator[VARTYPE]:
        """
        Show the progress of this iterator, without interfering the computation flow.

        For frozen generator, this will show a tqdm progress bar with percentage.
        """

        tqdm = _import_tqdm_module()

        def _(orig_gen):
            bar = tqdm(total=len(self.inner))
            item: VARTYPE
            for item in orig_gen:
                bar.update(1)
                yield item

        return MelodieGenerator(_(self.inner))

    def sort(
        self, key: Callable[[VARTYPE], Union[int, float, str, tuple]], reverse=False
    ) -> "MelodieFrozenGenerator[VARTYPE]":
        """
        Sort by key
        """
        new_list = [item for item in self.inner]
        new_list.sort(key=key, reverse=reverse)
        return MelodieFrozenGenerator(new_list)

    def relsort(
        self, cmp: Callable[[VARTYPE, VARTYPE], bool], reverse=False
    ) -> "MelodieFrozenGenerator[VARTYPE]":
        """
        Sort by relative comparisons
        """
        key = functools.cmp_to_key(cmp)
        new_list = [item for item in self.inner]
        new_list.sort(key=key, reverse=reverse)
        return MelodieFrozenGenerator(new_list)


T = TypeVar("T")


def compose(
    f_outer: Callable[..., T], *other_funcs: Callable[..., Any]
) -> Callable[..., T]:
    """
    Compose functions (from right to left)

    When function returns a tuple, the tuple will be automatically unpacked.
    To avoid this, just return a list.

    :type: Just a type annotation for the return-type of composed function.
    """

    def reducer(f, g):
        def wrapper(*x, **kwargs):
            ret = g(*x, **kwargs)
            if isinstance(ret, tuple):
                return f(*ret)
            else:
                return f(ret)

        return wrapper

    return functools.reduce(reducer, [f_outer] + list([*other_funcs]), lambda x: x)


def melodie_generator(
    f: "Callable[P, Union[Generator[VARTYPE, None, None], MelodieGenerator[VARTYPE]]]",
) -> "Callable[P, MelodieGenerator[VARTYPE]]":
    @functools.wraps(
        f,
        assigned=(
            ("__module__", "__name__", "__qualname__", "__doc__", "__annotation__")
        ),
    )
    def inner(*args, **kwargs):
        return MelodieGenerator(f(*args, **kwargs))

    return inner


def generator_next(g: Generator[VARTYPE, None, None]) -> Tuple[VARTYPE, bool]:
    try:
        return next(g), True
    except StopIteration:
        return None, False


def to_generator(it: Iterable[VARTYPE]) -> Generator[VARTYPE, None, None]:
    for item in it:
        yield item
