from ..e_typing import (
    ColorStdOut,
    NotIterable
)
from typing import (
    ParamSpec,
    Callable,
    TypeVar,
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
# Any Type
_AT = TypeVar('_AT')


def cprint(*args: _AT,
           color: str,
           undo_when_exit: bool = True) -> ColorStdOut[_AT]:
    "Print to Console in `Color of Custom`"
    print(color, end='')
    print(*args, end='')
    if undo_when_exit:
        print('\033[0m')


def gray(*values: _AT, default: bool = True) -> ColorStdOut[_AT]:
    "Print to Console in `Gray Color`"
    cprint(*values, color='\033[90m', undo_when_exit=default)


def red(*values: _AT, default: bool = True) -> ColorStdOut[_AT]:
    "Print to Console in `Red Color`"
    cprint(*values, color='\033[91m', undo_when_exit=default)


def green(*values: _AT, default: bool = True) -> ColorStdOut[_AT]:
    "Print to Console in `Green Color`"
    cprint(*values, color='\033[92m', undo_when_exit=default)


def yellow(*values: _AT, default: bool = True) -> ColorStdOut[_AT]:
    "Print to Console in `Yellow Color`"
    cprint(*values, color='\033[93m', undo_when_exit=default)


def blue(*values: _AT, default: bool = True) -> ColorStdOut[_AT]:
    "Print to Console in `Blue Color`"
    cprint(*values, color='\033[94m', undo_when_exit=default)


def magenta(*values: _AT, default: bool = True) -> ColorStdOut[_AT]:
    "Print to Console in `Magenta Color`"
    cprint(*values, color='\033[95m', undo_when_exit=default)


def turquoise(*values: _AT, default: bool = True) -> ColorStdOut[_AT]:
    "Print to Console in `Turquoise Color`"
    cprint(*values, color='\033[96m', undo_when_exit=default)


def border(*values: _AT, default: bool = True) -> ColorStdOut[_AT]:
    "Print to Console in `Border String`"
    cprint(*values, color='\033[97m', undo_when_exit=default)


class Color(NotIterable):
    "Constant of 'cprint' Function"
    blue = blue
    gray = gray
    green = green
    magenta = magenta
    red = red
    turquoise = turquoise
    yellow = yellow
    border = border


if __name__ == '__main__':
    blue('test', 'to', 'debug')
