from __future__ import annotations
from typing import ParamSpec, TypeVar, Callable, Any, Self, Iterable, Generator, Generic
from rich import print
from rich.table import Table
import inspect
import textwrap
import functools
import itertools
import dataclasses
import math
import dis
import ast

def Y(f):
    return (lambda x: f(lambda y: x(x)(y)))(lambda x: f(lambda y: x(x)(y)))


def apply(f):
    return lambda g: lambda *a, **k: f(g(*a, **k))


def _getattrs(obj: object) -> Iterable[str]:
    memory: set[str] = set()
    if hasattr(obj, "__dict__"):
        for key in getattr(obj, "__dict__").keys():
            memory.add(key)
    if hasattr(obj, "__slots__"):
        for name in getattr(obj, "__slots__"):
            memory.add(name)
    for name in dir(obj):
        memory.add(name)
    yield from memory


@dataclasses.dataclass(slots=True)
class Inspector:
    obj: object
    limit: int = 2
    name_rule: Callable[[int, str], bool] = lambda limit, name: True  # fmt: skip
    _memory: dict[str, Inspector] = dataclasses.field(default_factory=dict)

    def _build(self: Self, /, obj: object) -> None:
        for _attrname in _getattrs(obj):
            if self.name_rule(self.limit, _attrname):
                try:
                    self._memory[_attrname] = (
                        Inspector(
                            getattr(obj, _attrname), self.limit - 1, self.name_rule
                        )
                        if (self.limit - 1) != 0
                        else getattr(obj, _attrname)
                    )
                except AttributeError:
                    pass

    def __post_init__(self: Self, /) -> None:
        if self.limit > 0:
            self._build(self.obj)


def make_truthtable(
    function: FunctionType,
    args: Iterable[T] = range(2),
    retfmt: Callable = lambda v: str(int(v)),
) -> Table:
    sig = inspect.signature(function)
    table = Table()
    for argname in sig.parameters:
        table.add_column(argname)
    table.add_column(f"{function.__name__}({', '.join(sig.parameters.keys())})")
    for seq in itertools.product(args, repeat=len(sig.parameters)):
        table.add_row(*map(str, seq), retfmt(function(*seq)))
    return table

def ast_d(e):
    return ast.dump(ast.parse(e), indent=4)


def linspace(start, stop, step):
    buffer = start
    while buffer < stop:
        yield buffer
        buffer += step


def setget(self: dict, key: Any, value: T) -> T:
    self[key] = value
    return value


def taiwansort(arr, key=None, reverse=False):
    if sorted(arr, key=key, reverse=reverse) == arr:
        return arr
    else:
        raise SystemExit("4j1989y")


@lambda cls: cls()
class buffered:
    def get(self, key, default=None):
        return getattr(self, key, default)

    def pop(self, key, default=None):
        if hasattr(self, key):
            v = getattr(self, key)
            delattr(self, key)
            return v
        else:
            return default


def drop(*_, **__):
    pass


def enum(start: int = 0):
    yield from range(
        start,
        start
        + next(
            filter(
                lambda instruction: instruction.opname == "UNPACK_SEQUENCE",
                dis.get_instructions(inspect.stack()[1].frame.f_code),
            )
        ).argval,
    )


Param = ParamSpec("Param")
RetType0 = TypeVar("RetType0")
RetType1 = TypeVar("RetType1")
RetType2 = TypeVar("RetType2")
T = TypeVar("T")
W = TypeVar("W")

FunctionType = type(lambda _: _)
BuiltinF = type(sum)
FType = FunctionType | BuiltinF
CanCall = FType | type


def epsylon(e):
    def inner():
        return e

    return inner


def of_type(object, ret_type: type[T]) -> type[T]:
    return object  # xdd


# so(ource) : gl(obals) : lo(cals) : na(me) | de(dent) | as(ync)
def closure(
    σο: str,
    γλ: dict[str, Any] = globals(),
    λο: dict[str, object] = locals(),
    να: str = "Self",
    δε: bool = True,
    ασ: bool = False,
) -> Callable[Param, RetType0]:
    if δε is True:
        σο = textwrap.dedent(σο.strip("\n"))
    exec(f"{'async '*(ασ is True)}def {να}{σο}", γλ, λο)

    return λο[να]


def procedure(source: str, glob=globals(), loc=locals()):
    return closure(f"(*_,**__args):{source}")


def haskell(src, g=globals(), l=locals()):
    return eval(src.replace("\\", "lambda ", 1).replace("->", ":"), g, l)


def match(
    pattern: str, glob: dict[str, Any] = globals(), loc: dict[str, Any] = locals()
) -> FunctionType:
    def inner(expr: Any) -> T:
        source_lines: list[tuple[str, str]] = [
            (line.split("?")[1].split("->")[0].strip(), line.split("->")[1].strip())
            for line in textwrap.dedent(pattern.strip()).splitlines()
        ]
        buffered.__match_expr__ = expr
        thingy: str = "match buffered.__match_expr__:" + (
            "".join(
                f"\n\tcase {c}:\n\t\tbuffered.__match_result__={e}"
                for c, e in source_lines
            )
        )

        exec(thingy, glob, loc)
        v = buffered.pop("__match_result__", None)
        return v

    return inner


def whle(
    conditionfunction: Callable[Param, bool],
    runfunction: Callable[Param, RetType0],
    argfunction: Callable[Param, RetType1] | None = None,
) -> Generator[RetType0, None, None]:
    while conditionfunction():
        yield runfunction(argfunction()) if argfunction is not None else runfunction()


def tryexcept(
    exception_or_group: Exception | tuple[Exception, ...],
    tryblock: Any | Callable[Param, RetType0],
    exceptblock: Any | Callable[Param, RetType1] | None = None,
) -> Any | RetType0 | RetType1:
    try:
        return tryblock() if callable(tryblock) else tryblock
    except exception_or_group:
        return (
            exceptblock()
            if callable(exceptblock)
            else exceptblock
            if exceptblock is not None
            else None
        )


def compose_two(f, g):
    return functools.wraps(f)(lambda *args, **kwargs: f(g(*args, **kwargs)))


def compose(*fns):
    return functools.reduce(compose_two, reversed(fns))


def silent(
    f: Callable[Param, RetType0], *args: tuple[Any, ...], **kwargs: dict[str, Any]
) -> None:
    f(*args, **kwargs)


def repeat(func, item, times: int):
    for _ in range(times):
        item = func(item)
    return item


def strsub(self: str, other: str) -> str:
    return self[: (idx := self.find(other))] + self[idx + len(other) :]


def scan(
    self: Callable[[list[T]], W], iterable: Iterable[T]
) -> Generator[W, None, None]:
    buffer = []
    for item in iterable:
        buffer.append(item)
        yield self(buffer)


def bmask(self, mask: Iterable[bool]):
    for item, mask in zip(self, mask):
        if mask:
            yield item


def for_each(self, func: CanCall):
    for el in self:
        func(el)


def ϟ(self, func: CanCall):  # funny name alias
    return for_each(self, func)


def chunk_by(self, n: int):
    yield from zip(*[iter(self)] * n)


def extendw(self, other):
    return itertools.chain(iter(self), iter(other))


def e(self, other):
    return extendw(self, other)


def builder(pattern="with_"):
    return type(
        "builder",
        (),
        {
            "__getattribute__": lambda self, __name: (
                lambda value: [setattr(self, __name[len(pattern) :], value), self][-1]
            )
            if __name.startswith(pattern)
            else object.__getattribute__(self, __name)
        },
    )


class Church:
    __slots__ = ("x", "f", "__dict__")

    @functools.cache
    def __repr__(self) -> str:
        if self.x < 1:
            return f"λf.λx.{'f '*self.x}x"
        else:
            buffer = "".join(f"f{'('*(x!=self.x-1)}" for x in range(self.x))
            return f"λf.λx.{buffer} x{')'*(self.x-1)}"

    @functools.cache
    def __call__(self: Self, n: int):  # me when repeat
        buf = self.x
        for _ in range(n):
            buf = self.f(buf)
        return Church(x=buf)

    @staticmethod
    def bindop(op: FType):
        return lambda self, other: Church(
            lambda n: op(self.f(n), other.f(n)), op(self.x, other.x)
        )

    def __init__(self, f=lambda n: n + 1, x=0):
        return [setattr(self, "f", f), setattr(self, "x", x)][-1]

    __add__ = bindop(lambda x, y: x + y)
    __sub__ = bindop(lambda x, y: x - y)
    __mul__ = bindop(lambda x, y: x * y)
    __pow__ = bindop(lambda x, y: x**y)
    __truediv__ = bindop(lambda x, y: x / y)
    __floordiv__ = bindop(lambda x, y: x // y)

    def __eq__(self, other):
        return (self.x, self.f) == (other.x, other.f)

    def __hash__(self):
        return hash((self.f, self.x)) + 42


@dataclasses.dataclass(slots=True)
class option(Generic[T]):
    @classmethod
    def from_call(
        cls, func: Callable[[ParamSpec], W], *args: ParamSpec, **kwargs: ParamSpec
    ) -> option[W]:
        try:
            result = func(*args, **kwargs)
            return yes(result)
        except Exception:
            return no()

    def unwrap(self, msg="Failed to unwrap") -> T:
        match self:
            case yes(value):
                return value
            case no():
                raise ValueError(msg)

    def unwrap_or(self, default: W) -> T | W:
        match self:
            case yes(value):
                return value
            case no():
                return default

    def is_yes(self) -> bool:
        return isinstance(self, yes)

    def is_no(self) -> bool:
        return isinstance(self, no)  # ?asd/a

    def waste(self) -> option:
        return no()

    def bind(self, func: Callable[[T], W]) -> option[W]:
        match self:
            case yes(value):
                return type(self).from_call(func, value)
            case no():
                return no()

    def bind_val(self, value: W) -> option[W]:
        return yes(value)

    def bind_if_no(self, value: W) -> option[T | W]:
        if self.is_no():
            return yes(value)
        else:
            return self
        
    def __bool__(self) -> bool:
        return self.is_yes()

@dataclasses.dataclass
class yes(option[Generic[T]]):  # :)
    value: T

@dataclasses.dataclass
class no(option):  # :(
    ...


# --->


def cmp(x: Any, y: Any) -> int | None:
    if x < y:
        return 1
    if x > y:
        return -1
    if x == y:
        return 0
    return None


@dataclasses.dataclass
class space:
    obj: object

    def __getitem__(self, name_chain: slice | tuple[slice, ...]) -> object:
        if isinstance(name_chain, slice):
            if isinstance(name_chain.step, str):
                return getattr(self.obj, name_chain.step)
            else:
                buffer = self.obj
                for name in name_chain.step:
                    buffer = getattr(buffer, name)
                return buffer
        else:
            buffer = self.obj  # {
            for name in name_chain:  #   can functools reduce
                buffer = getattr(buffer, name.step)  #   somehow i guess
            return buffer  # }

        # reduce(lambda buffer, name: getattr(buffer, name.step), name_chain, self.obj) # by hmp, sadly cant debug


@dataclasses.dataclass
class using:
    obj: object
    namespace: dict[str, object]
    buffered: set[str] = dataclasses.field(default_factory=set)

    def __enter__(self):
        for key in _getattrs(self.obj):
            if key not in self.namespace:
                self.namespace[key] = getattr(self.obj, key)
                self.buffered.add(key)

    def __exit__(self, *_):
        for key in self.buffered:
            if key in self.namespace:
                self.namespace.pop(key)


# stuff in comments is default wincompose bindings
# [greek] [fp]
λ = closure  # *l
ι = compose  # *i
ε = epsylon  # *e
ζ = list  # *z
Σ = sum  # *S
μ = map  # *m
γ = __import__  # *g
Δ = range  # *D
Π = print  # *P
φ = filter  # *f
ρ = functools.reduce  # *r
ξ = "".join  # *j
Ξ = " ".join  # *J
ς = functools.partial  # *w
π = bmask  # *p
η = chr  # *h
κ = ord  # *k
σ = sorted  # *s
χ = scan  # *x
α = ι(φ, ζ)  # *a [filter -> list]
β = ι(μ, ζ)  # *b [map -> list]
ψ = ι(π, ζ)  # *c [bmask -> list]
δ = ι(χ, ζ)  # *d [scan -> list]
τ = lambda d, b, n = "": type(n, b, d)  # fmt: skip
θ = zip  # *u
σγ = setget
# [english] [math]
s = math.sqrt
p = math.prod
c = math.comb
l2 = math.log2
ln = math.log
lg = math.log10

# [english] [types and some builtins]
ﬆ = str  # st
ı = int  # .i
İ = input  # .I
ɨ = iter  # /i
ē = enumerate  # -e

# [chinese / jp]
ha = haskell  # chinese a

def it(s=0):
    return enumerate(iter(int, -~int()), start=s)  # japanese i


def itn(s=0):
    return lambda x=it(s=s): next(x)[0]  # japanese i+n


def ga(n):
    return lambda o: getattr(o, n)  # chinese g->


def sa(o, n, f=sum):
    return f(map(ga(n), o))  # chinese s->


# [english] [random aliases because xd]
g = globals
l = locals
d = drop
w = whle
ṗ = procedure  # .p
