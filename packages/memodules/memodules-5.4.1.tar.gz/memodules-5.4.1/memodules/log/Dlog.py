from ..e_typing import (
    ColorStdOut,
    CanStdOut,
    StdOut,
)
from functools import wraps
from typing import (
    ParamSpec,
    Callable,
    Optional,
    TypeVar,
    TypeVarTuple,
)
from .cprint import (
    Color,
)
import sys
__all__ = [
    'DebugPrint',
    'log',
]
_Args = ParamSpec('_Args')
_Returns = TypeVar('_Returns')


def log(cfunc: Optional[Callable[_Args, _Returns]] = None, /,
        *, debugging: bool = True,
        color: Color = Color.blue,
        show_caller: bool = True,
        show_called: bool = True,
        show_args: bool = True,
        show_returns: bool = True) -> Callable[_Args, _Returns]:
    "develop"
    @wraps(cfunc)
    def decorator(func: Callable[_Args, _Returns]) -> Callable[_Args, _Returns]:
        if not debugging: return func
        @wraps(func)
        def wrapper(*args: _Args.args, **kwargs: _Args.kwargs) -> _Returns:
            show = ''
            flg = False
            if show_caller:
                c_frame = sys._getframe(1)
                _mid = f'{c_frame.f_globals["__name__"]}.'
                _mid += f'{c_frame.f_code.co_name}'
                show += f'Caller: {_mid}'
                del _mid
                flg = True
            if show_called:
                if flg:
                    show += '\n'
                show += f'Called: {func.__name__}'
                flg = True
            if show_args:
                if flg:
                    show += '\n'
                show += f'Args: {args}, {kwargs}'
                flg = True
            if flg:
                color(show)
                del show, flg
            result = func(*args, **kwargs)
            if show_returns:
                color(f'Returns: {result}')
            return result
        return wrapper

    if cfunc is not None:
        return decorator(cfunc)

    return decorator


args = TypeVarTuple('args')


class DebugPrint:
    __slots__ = ('debug', 'nl_num')

    def __init__(self, debug_flg: bool, newline_number: int = 3):
        """デバッグ用ログをデバッグフラグがTrueならcall構文で指定した引数の内容を色違いでコンソール出力してくれるクラス\n
        出力する項目をnewline_number個ごとに改行して出力を見やすくする"""
        self.debug = debug_flg
        self.nl_num = newline_number

    def __call__(self, *args: *args) -> ColorStdOut[*args]:
        """examples:
            >>> debug = DebugPrint(True)
            >>> debug('debug', 'to', 'example')
            (light green)debug: debug, to, example
            >>> debug = DebugPrint(True, newline_number = 2)
            >>> debug('debug', 'to', 'example')
            debug: debug, to,
            \texample"""
        nt = '\n\t'
        spc = ' '
        if self.debug:
            for i in range(len(args)):
                if i == 0:
                    content = args[i]
                else:
                    mid_entry = nt if i % self.nl_num == 0 else spc
                    content = f'{content},{mid_entry}{args[i]}'

            print(f'\033[92mdebug: {content}\033[0m')
