"""It provides an extra class that has no function and can only be used for type hints.\n
何の機能も無い、型ヒントだけに使えるエクストラなクラスを提供するやで。"""
from typing import (
    TypeVarTuple,
    Callable,
    Generic,
    TypeVar,
    Any,
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
_ET = TypeVar('_ET')
_ATs = TypeVarTuple('_ATs')
_F = TypeVar('_F', bound=Callable[..., Any])


class Function(Callable[_F, _AT]):
    def __getitem__(self, key: _F) -> _AT:
        ...


class NotIterable:
    """Mixin to prevent iteration, without being compatible with Iterable.

    That is, we could do:
        def __iter__(self): raise TypeError()
    But this would make users of this mixin duck type-compatible with
    collections.abc.Iterable - isinstance(foo, Iterable) would be True.

    Luckily, we can instead prevent iteration by setting __iter__ to None, which
    is treated specially.
    """

    __slots__ = ()
    __iter__ = None


class StdOut(Generic[*_ATs]):
    '<TypeHints to indicate that it will be printed to the console>'
    def __str__(self) -> str:
        return '<type hints StdOut>'

    def __repr__(self) -> str:
        return self.__doc__


class ColorStdOut(StdOut[*_ATs], Generic[*_ATs]):
    def __str__(self) -> str:
        return '<type hints ColorStdOut>'


class CanStdOut(Generic[*_ATs]):
    ...


class SupportIndex(Generic[*_ATs]):
    ...

class SupportPath(Generic[*_ATs]):
    ...
