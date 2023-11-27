"""It provides an extra class that has no function and can only be used for type hints.\n
何の機能も無い、型ヒントだけに使えるエクストラなクラスを提供するやで。"""
from typing import (
    _SpecialForm,
    TypeVarTuple,
    ParamSpec,
    Callable,
    Sequence,
    Generic,
    TypeVar,
)
from sys import (
    stdout,
    __stdout__
)
__all__ = [
    'ColorStdOut',
    'NotIterable',
    'StdOut',
    'SupportIndex',
    'SupportPath',
    'Indexes',
    'Pathes'
]


_AT = TypeVar('_AT')  # T は任意の型を表す型変数
_ATs = TypeVarTuple('_ATs')
_AT_co = TypeVar('_AT_co', covariant=True)


values = TypeVarTuple('values')
default = TypeVar('default', bound=bool)
a: Callable[[*values, default], str]


arg_names = TypeVarTuple('arg_names')
return_type = TypeVar('return_type')


class Function(Callable[[*arg_names], return_type]):
    "developing now"
    ...


class NotIterable:
    """Mixin to prevent iteration, without being compatible with Iterable.
    Iterable との互換性がなく、繰り返しを防止するためにミックスインします。

    That is, we could do:
    つまり、次のことができます:
        def __iter__(self): raise TypeError()
    But this would make users of this mixin duck type-compatible with
    collections.abc.Iterable - isinstance(foo, Iterable) would be True.

    Luckily, we can instead prevent iteration by setting __iter__ to None,
    which is treated specially.
    """

    __slots__ = ()
    __iter__ = None


class StdOut(Generic[*_ATs]):
    'TypeHints to indicate that it will be printed to the console'
    def __str__(self) -> str:
        return '<type hints StdOut>'

    def __repr__(self) -> str:
        return f'<{self.__doc__}>'


class ColorStdOut(StdOut[*_ATs], Generic[*_ATs]):
    'TypeHints to indicate that it will be printed of ColorString to the console'
    def __str__(self) -> str:
        return '<type hints ColorStdOut>'


class CanStdOut(Generic[*_ATs]):
    ...


class SupportIndex(Generic[*_ATs]):
    ...


class SupportPath(Generic[*_ATs]):
    ...
