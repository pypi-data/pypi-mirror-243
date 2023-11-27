from collections import namedtuple
from functools import wraps
from ...memodules.log import cprint
from ..e_typing import (
    ColorStdOut,
    NotIterable,
    Function,
)
from typing import (
    NamedTuple,
    ParamSpec,
    ParamSpecArgs,
    ParamSpecKwargs,
    Callable,
    Generic,
    TypeVar,
    get_args,
    Any,
)
__all__ = [
    # const
    'Color',

    # functions
    # #custom
    'cprint',

    # #presets
    'blue',
    'gray',
    'green',
    'magenta',
    'red',
    'turquoise',
    'yellow',

    # #decoration
    'border',
]
_AT = TypeVar('_AT', bound=Callable[..., Any])


def cprint(*args: _AT,
           color: str,
           undo_when_exit: bool = True) -> ColorStdOut[_AT]:
    "Print to Console in `Color of Custom`"
def gray(*values: _AT, default: bool = True) -> ColorStdOut[_AT]:
    "Print to Console in `Gray Color`"
def red(*values: _AT, default: bool = True) -> ColorStdOut[_AT]:
    "Print to Console in `Red Color`"
def green(*values: _AT, default: bool = True) -> ColorStdOut[_AT]:
    "Print to Console in `Green Color`"
def yellow(*values: _AT, default: bool = True) -> ColorStdOut[_AT]:
    "Print to Console in `Yellow Color`"
def blue(*values: _AT, default: bool = True) -> ColorStdOut[_AT]:
    "Print to Console in `Blue Color`"
def magenta(*values: _AT, default: bool = True) -> ColorStdOut[_AT]:
    "Print to Console in `Magenta Color`"
def turquoise(*values: _AT, default: bool = True) -> ColorStdOut[_AT]:
    "Print to Console in `Turquoise Color`"
def border(*values: _AT, default: bool = True) -> ColorStdOut[_AT]:
    "Print to Console in `Border String`"
Color = NamedTuple('Color', [
    ('blue', type(blue)), ('gray', type(gray)), ('green', type(green)), ('magenta', type(magenta)), ('red', type(red)), ('turquoise', type(turquoise)), ('yellow', type(yellow)), ('border', type(border))])
Color = Color(blue, gray, green, magenta, red, turquoise, yellow, border)
Color.__doc__ = "Constant of 'cprint' Function"
