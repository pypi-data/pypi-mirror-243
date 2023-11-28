"""規模の小さいアプリケーションでたまに許されてる.iniのセクション被り対応版ini controller"""
# region	|=-=-=-=|Import  Section|=-=-=-=|
from collections import namedtuple
from typing import (
    NamedTuple,
    overload,
    Literal,
    TextIO,
    AnyStr,
    Any,
    IO,
)
import __init__
from types import ModuleType
# endregion
# 			|=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=|

# region	|=-=-=-=|Setup Section|=-=-=-=|
__all__ = [
    'Encoding',
    'INIsNotFound',
    'INI',
    'AbsTrue',
    'AbsFalse',
    'AbsTrueFalse',
    'StrBool',
    'str_bool'
]
ini_item_string = type('ini_format_string', (str,))
ini_section_string = type('ini_format_string', (str,))


class Encoding(NamedTuple):
    SJIS: str
    UTF8: str


Encoding = Encoding(...)
# endregion
# 			|=-=-=-=-=-=-=-=-=-=-=-=-=-=-=|


# iniファイルない時用の例外
class INIsNotFound(Exception):
    '''Required :ref:`.ini` Files Does Not Exist'''
    # .iniファイル必要なのに無いやで。ってやつ

    # classに直接文字列要求(例: str(), print(), raise)があったときに自動で処理される特殊メソッド
    def __str__(self) -> str: ...


# 大本営
class INI:
    def __init__(self, filepath: str = None, encoding: str = 'shift-jis') -> None:
        """.iniファイル編集するのに便利系クラス\n
        Parameters:
            filepath (str): 読み込みたい.iniのフルパス。`None`で`raise`\n
            encoding (str): 読み込むファイルのエンコード方式。現状、書き出しと共通設定。未指定時 -> `shift-jis`"""
        if filepath is not None:
            self.file_path: str
            self.out_file: str
        self.chrdec: str
        self._context: bool
        self.ini_content: dict
        self._already_exist: dict
        self._exist_lower: dict

    def _keys(self, ini_contents: dict = ...) -> list:
        """dictの第一keyをlistで返すやつ\n
        Examples:
            >>> fruit_dict = \
{'apple': 'red', 'banana': 'yellow', 'orange': 'orange'}
            >>> _sections(fruit_dict)
            ['apple', 'banana', 'orange']"""
        ...

    def _ini_item(self, item: str = ..., value: str = ...) -> ini_item_string:
        """itemとvalueを'='でつないで.iniフォーマットにして返す\n
        Example:
            >>> _ini_item('apple', 'red')
            'apple=red'"""
        ...

    def _item(self, sect, items: tuple[str, Any] = ...) -> None: ...
    def _section(self, name: str = ...) -> None: ...

    def _section_wrapp(self, key: str) -> ini_section_string:
        """dictの第一key(セクション名)を.iniのセクション用にラップするやつ\n
        Example:
            >>> _section_wrapp('section')
                -> '[section]'"""
        ...

    def _write_section(self, section: str = ..., wrapp: bool = False) -> str | ini_section_string:
        """ダブりセクションがあったときに一時的にリネームして保持するから、
        それを本来のセクション名に戻して返すメソッド。ダブってなかったらArg=return\n
        wrapp=Trueで_section_wrapp()も一緒に処理して返す。
        Example:
            example.ini:
                [section]\n
                apple=red\n
                banana=yellow\n
                ...\n
                [section]\n
                orange=orange\n
                [anysection]\n
                ...\n
            >>> ini = \
{'section': {'apple': 'red', 'banana': 'yellow', ...},\\\n
            >>>        'section1': {'orange': 'orange'},\\\n
            >>>        'anysection': ...}
            >>> _write_section('section1')
                -> 'section'
            >>> _writesection('anysection', wrapp=True)
                -> '[anysection]'"""
        ...

    def config(self, OutputPath: str = None) -> None: ...

    def export(self) -> TextIO:
        """configで設定した出力ファイルに.iniフォーマットで編集した内容を書き出す。
        出力ファイルを設定してなかったら元ファイルを上書き"""
        ...

    def isexist(self, key: str) -> str:
        """### :code:`key in self._already_exist` ⇓ \n
        Returns:
            renamed key

        ### :code:`key not in self._already_exist` ⇓ \n
        Returns:
            input to arg key"""
        ...

    def read(self, ini_file: IO = None) -> dict[dict[AnyStr, ...], ...] | Exception: ...
    @overload
    def __getitem__(self, key: tuple[str, str]) -> dict | str | None: ...
    @overload
    def __getitem__(self, key: str = '*') -> dict[dict, ...]: ...
    @overload
    def __getitem__(self, key: str = AnyStr) -> None | dict: ...
    @overload
    def __getitem__(self, key=None) -> None: ...
    def __setitem__(self, key: tuple[str, str], value) -> None: ...
    def __enter__(self) -> 'ini':
        self._context = True
        self.file = open(self.file_path, encoding=self.chrdec)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.file.close()


class _StrOrBool:
    def __init__(self, content: '_StrOrBool'):
        self.content = content

    def STRING(self, content: '_StrOrBool' = None):
        ...

    def BOOL(self, content: '_StrOrBool' = None):
        ...

    def __str__(self):
        """
        Example:
            _SubStrOrBool_instance << str('true')
            >>> print(str(_SubStrOrBool_instance))
            bool(True)
        """
        return self.STRING(self.content)

    def __init_true__(self):
        class _true:
            def __init__(subself):
                subself.trues = (True, 1, 'true', '1')

            @property
            def true(subself):
                return subself.trues

            def __contain__(subself, item: str | bool | int):
                if isinstance(item, str):
                    return item.lower() in subself.trues
                else:
                    return item in subself.trues

        return _true()

    def __init_false__(self):
        class _false:
            def __init__(subself):
                subself.falses = (False, 0, 'false', '0', None)

            @property
            def false(subself):
                return subself.falses

            def __contain__(subself, item: str | bool | int):
                if isinstance(item, str):
                    return item.lower() in subself.falses
                else:
                    return item in subself.falses

        return _false()

    def __init_subclass__(cls, *args, **kwargs) -> None:
        super().__init_subclass__(*args, **kwargs)
        cls.true = cls.__init_true__(cls)
        cls.false = cls.__init_false__(cls)

    @property
    def trues(self):
        return self.__init_true__().trues

    @property
    def falses(self):
        return self.__init_false__().falses


class AbsTrue(_StrOrBool):
    def __init__(self, content: _StrOrBool):
        super().__init__(content)

    def __bool__(self) -> bool:
        return self.content in self.true


class AbsFalse(_StrOrBool):
    def __init__(self, content: _StrOrBool):
        super().__init__(content)

    def __bool__(self) -> bool:
        return self.content in self.false


class AbsTrueFalse(_StrOrBool):
    def __init__(self, content: _StrOrBool):
        super().__init__(content)

    def __bool__(self) -> bool:
        if self.content in self.true:
            return True
        elif self.content in self.false:
            return False
        else:
            return None


class StrBool:
    def __new__(cls, content: _StrOrBool, absolute: bool = None) -> AbsTrue | AbsFalse | AbsTrueFalse: ...


def str_bool(content: str):
    trues = (True, 1, 'true', '1')
    falses = (False, 0, 'false', '0', None)

    if content.lower() in trues:
        return True
    elif content.lower() in falses:
        return False
    else:
        return None
